from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'profiles', views.ArtistProfileViewSet)
router.register(r'reviews', views.ArtistReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
