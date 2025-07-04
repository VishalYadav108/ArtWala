from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import CommissionRequest, CommissionProposal, CommissionContract, CommissionMilestone
from .serializers import CommissionRequestSerializer, CommissionProposalSerializer, CommissionContractSerializer, CommissionMilestoneSerializer

class CommissionRequestViewSet(viewsets.ModelViewSet):
    queryset = CommissionRequest.objects.all()
    serializer_class = CommissionRequestSerializer
    permission_classes = [AllowAny]

class CommissionProposalViewSet(viewsets.ModelViewSet):
    queryset = CommissionProposal.objects.all()
    serializer_class = CommissionProposalSerializer
    permission_classes = [AllowAny]

class CommissionContractViewSet(viewsets.ModelViewSet):
    queryset = CommissionContract.objects.all()
    serializer_class = CommissionContractSerializer
    permission_classes = [AllowAny]

class CommissionMilestoneViewSet(viewsets.ModelViewSet):
    queryset = CommissionMilestone.objects.all()
    serializer_class = CommissionMilestoneSerializer
    permission_classes = [AllowAny]
