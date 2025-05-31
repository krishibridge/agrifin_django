from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Farm
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
        queryset=User.objects.filter(role="farmer"),
        required=False, 
        source='owner.get_full_name'
    )
    class Meta:
        model = Farm
        fields = ["id", "owner", "location", "size"]
        read_only_fields = [] 
