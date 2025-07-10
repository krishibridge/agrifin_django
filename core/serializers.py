from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Device, User, Farm
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "phone_number",
            "first_name",
            "last_name",
            "email",
            "role",
            "address",
            "aadhaar_number",
            "profile_image",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "phone_number",
            "first_name",
            "last_name",
            "email",
            "password",
            "role",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # `data` now has 'access' and 'refresh'
        user_data = UserSerializer(self.user).data
        data.update({"user": user_data})
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            phone_number=data["phone_number"], password=data["password"]
        )
        if not user:
            raise serializers.ValidationError("Invalid phone number or password")
        data["user"] = user
        return data


class FarmSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role="farmer"), required=False
    )
    owner_name = serializers.CharField(source="owner.get_full_name", read_only=True)

    class Meta:
        model = Farm
        fields = ["id", "owner", "owner_name", "location", "size"]
        read_only_fields = ["owner_name"]


class DeviceSerializer(serializers.ModelSerializer):
    # For reads, you can still expose the farm’s location if you like:
    farm_location = serializers.CharField(
        source='farm.location',
        read_only=True
    )

    # For writes, accept a farm pk
    farm = serializers.PrimaryKeyRelatedField(
        queryset=Farm.objects.all(),
        allow_null=True,
        required=False
    )

    class Meta:
        model = Device
        # note: include both farm (writable) and farm_location (readable) if you want
        fields = ['id', 'device_name', 'farm', 'farm_location', 'installed_on', 'status']
        read_only_fields = ['installed_on']
