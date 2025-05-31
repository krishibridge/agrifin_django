from rest_framework import serializers
from .models import Device, SoilData, EnvironmentData, VisionData

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class SoilDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilData
        fields = '__all__'

class EnvironmentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvironmentData
        fields = '__all__'

class VisionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisionData
        fields = '__all__'
