from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'chapters', views.ChapterViewSet)
router.register(r'events', views.ChapterEventViewSet)
router.register(r'memberships', views.ChapterMembershipViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
