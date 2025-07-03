from rest_framework import serializers
from .models import ArtistProfile, ArtistReview
from users.serializers import UserSerializer

class ArtistProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ArtistProfile
        fields = '__all__'
        read_only_fields = ['slug', 'rating', 'total_reviews', 'created_at', 'updated_at']

class ArtistReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)
    
    class Meta:
        model = ArtistReview
        fields = '__all__'
        read_only_fields = ['reviewer', 'created_at']
