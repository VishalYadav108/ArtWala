from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'profiles', views.ArtistProfileViewSet)
router.register(r'reviews', views.ArtistReviewViewSet)
router.register(r'followings', views.ArtistFollowingViewSet, basename='artist-following')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.ArtistRegistrationView.as_view(), name='artist-register'),
    path('login/', views.ArtistLoginView.as_view(), name='artist-login'),
]
