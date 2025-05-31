# core/views.py
from rest_framework import generics, mixins
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from .models import User, Farm


# 1) Registration still uses your RegisterSerializer
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


# 2) Replace your old LoginView with the JWT view
class LoginView(MyTokenObtainPairView):
    permission_classes = [AllowAny]


# 3) Refresh endpoint
class LoginRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


class UserListCreateView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RegisterSerializer
        return UserSerializer

    def get_queryset(self):
        if self.request.user.role == "admin":
            return User.objects.all()
        return User.objects.filter(pk=self.request.user.pk)

    # hook up GET
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # hook up POST
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


# 4) Profile
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# 5) Farms
class FarmListCreateView(generics.ListCreateAPIView):
    serializer_class = FarmSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == "admin":
            return Farm.objects.all()
        return Farm.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        if self.request.user.role == "admin" and "owner" in self.request.data:
            serializer.save()
        else:
            serializer.save(owner=self.request.user)


class FarmDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FarmSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == "admin":
            return Farm.objects.all()
        return Farm.objects.filter(owner=self.request.user)

    def perform_update(self, serializer):
        if self.request.user.role == "admin" and "owner" in self.request.data:
            serializer.save()
        else:
            serializer.save()
