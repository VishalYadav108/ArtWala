from rest_framework import serializers
from .models import ArtistProfile, ArtistReview, ArtistFollowing
from users.serializers import UserSerializer
from users.models import User
from django.contrib.auth import authenticate
from django.utils.text import slugify

class ArtistProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ArtistProfile
        fields = '__all__'
        read_only_fields = ['slug', 'rating', 'total_reviews', 'created_at', 'updated_at']

class ArtistRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    display_name = serializers.CharField(required=True)
    
    class Meta:
        model = ArtistProfile
        fields = ['email', 'password', 'password_confirm', 'display_name', 'tagline', 
                 'specializations', 'experience_years', 'bio', 'website']
    
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError("Password and confirmation don't match.")
        return attrs
    
    def create(self, validated_data):
        # Extract user data
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        validated_data.pop('password_confirm')
        
        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            user_type='artist'
        )
        
        # Create artist profile
        display_name = validated_data.get('display_name')
        slug = slugify(display_name)
        
        # Ensure slug is unique
        base_slug = slug
        counter = 1
        while ArtistProfile.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
            
        artist_profile = ArtistProfile.objects.create(
            user=user,
            slug=slug,
            **validated_data
        )
        
        return artist_profile

class ArtistLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('User account is disabled.')
                
                try:
                    artist_profile = user.artist_profile
                except ArtistProfile.DoesNotExist:
                    raise serializers.ValidationError('User is not registered as an artist.')
                
                attrs['user'] = user
            else:
                raise serializers.ValidationError('Invalid credentials.')
        else:
            raise serializers.ValidationError('Must include email and password.')
        
        return attrs

class ArtistReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)
    
    class Meta:
        model = ArtistReview
        fields = '__all__'
        read_only_fields = ['reviewer', 'created_at']

class ArtistFollowingSerializer(serializers.ModelSerializer):
    follower_username = serializers.CharField(source='follower.username', read_only=True)
    artist_name = serializers.CharField(source='artist.display_name', read_only=True)
    
    class Meta:
        model = ArtistFollowing
        fields = ['id', 'follower', 'artist', 'follower_username', 'artist_name', 'created_at']
        read_only_fields = ['created_at']
