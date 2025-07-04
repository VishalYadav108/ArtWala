from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'forums', views.ForumViewSet)
router.register(r'posts', views.ForumPostViewSet)
router.register(r'jobs', views.JobPostingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
