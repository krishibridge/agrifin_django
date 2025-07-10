from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

class SensorDataView(APIView):
    def get(self, request):
        device_id = request.query_params.get('device_id')
        if not device_id:
            return Response({'error': 'device_id is required'}, status=400)

        try:
            device = Device.objects.get(id=device_id)
        except Device.DoesNotExist:
            return Response({'error': 'Device not found'}, status=404)

        latest_soil = SoilData.objects.filter(device=device).last()
        latest_env = EnvironmentData.objects.filter(device=device).last()

        data = {
            "soil": SoilDataSerializer(latest_soil).data if latest_soil else None,
            "environment": EnvironmentDataSerializer(latest_env).data if latest_env else None,
        }
        return Response(data)

    def post(self, request):
        device_id = request.data.get('device_id')
        if not device_id:
            return Response({'error': 'device_id is required'}, status=400)

        try:
            device = Device.objects.get(id=device_id)
        except Device.DoesNotExist:
            return Response({'error': 'Device not found'}, status=404)

        response_data = {}

        if 'soil' in request.data:
            soil_data = request.data['soil']
            soil_data['device'] = device.id
            soil_serializer = SoilDataSerializer(data=soil_data)
            if soil_serializer.is_valid():
                soil_serializer.save()
                response_data['soil'] = 'Soil data saved'
            else:
                response_data['soil'] = soil_serializer.errors

        if 'environment' in request.data:
            env_data = request.data['environment']
            env_data['device'] = device.id
            env_serializer = EnvironmentDataSerializer(data=env_data)
            if env_serializer.is_valid():
                env_serializer.save()
                response_data['environment'] = 'Environment data saved'
            else:
                response_data['environment'] = env_serializer.errors

        if not response_data:
            return Response({'error': 'No valid sensor data provided'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(response_data, status=status.HTTP_201_CREATED)

class VisionDataView(APIView):
    def get(self, request):
        device_id = request.query_params.get('device_id')
        if not device_id:
            return Response({'error': 'device_id is required'}, status=400)

        try:
            device = Device.objects.get(id=device_id)
        except Device.DoesNotExist:
            return Response({'error': 'Device not found'}, status=404)

        latest_vision = VisionData.objects.filter(device=device).last()
        data = VisionDataSerializer(latest_vision).data if latest_vision else None
        return Response({"vision": data})

    def post(self, request):
        device_id = request.data.get('device_id')
        if not device_id:
            return Response({'error': 'device_id is required'}, status=400)

        try:
            device = Device.objects.get(id=device_id)
        except Device.DoesNotExist:
            return Response({'error': 'Device not found'}, status=404)

        vision_data = request.data
        vision_data['device'] = device.id
        vision_serializer = VisionDataSerializer(data=vision_data)
        if vision_serializer.is_valid():
            vision_serializer.save()
            return Response({'vision': 'Vision data saved'}, status=status.HTTP_201_CREATED)
        else:
            return Response(vision_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
