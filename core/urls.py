from django.urls import path
from .views import *

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", LoginRefreshView.as_view(), name="token_refresh"),

    path("user/", UserListCreateView.as_view(), name="user-list-create"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user-detail"),

    path("profile/", UserProfileView.as_view(), name="user-profile"),
    
    path("farm/", FarmListCreateView.as_view(), name="farm-list-create"),
    path("farm/<int:pk>/", FarmDetailView.as_view(), name="farm-detail"),
    path('device/', DeviceView.as_view(), name='device-data'),
]
