from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


router = DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('api/profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),     # Login → get access & refresh tokens
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    # Refresh token
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),       # (Optional) Verify if token is valid
    
]
