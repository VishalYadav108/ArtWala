from rest_framework import serializers
from .models import CommissionRequest, CommissionProposal, CommissionContract, CommissionMilestone, CommissionPayment, CommissionReview

class CommissionRequestSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.get_full_name', read_only=True)
    proposals_count = serializers.SerializerMethodField()
    
    class Meta:
        model = CommissionRequest
        fields = '__all__'
    
    def get_proposals_count(self, obj):
        return 1 if hasattr(obj, 'proposal') and obj.proposal else 0

class CommissionProposalSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.display_name', read_only=True)
    request_title = serializers.CharField(source='request.title', read_only=True)
    
    class Meta:
        model = CommissionProposal
        fields = '__all__'

class CommissionContractSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.get_full_name', read_only=True)
    artist_name = serializers.CharField(source='artist.display_name', read_only=True)
    
    class Meta:
        model = CommissionContract
        fields = '__all__'

class CommissionMilestoneSerializer(serializers.ModelSerializer):
    contract_title = serializers.CharField(source='contract.title', read_only=True)
    
    class Meta:
        model = CommissionMilestone
        fields = '__all__'

class CommissionPaymentSerializer(serializers.ModelSerializer):
    contract_title = serializers.CharField(source='contract.title', read_only=True)
    
    class Meta:
        model = CommissionPayment
        fields = '__all__'

class CommissionReviewSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.get_full_name', read_only=True)
    artist_name = serializers.CharField(source='artist.display_name', read_only=True)
    
    class Meta:
        model = CommissionReview
        fields = '__all__'
