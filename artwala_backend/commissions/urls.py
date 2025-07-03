from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'requests', views.CommissionRequestViewSet)
router.register(r'proposals', views.CommissionProposalViewSet)
router.register(r'contracts', views.CommissionContractViewSet)
router.register(r'milestones', views.CommissionMilestoneViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
