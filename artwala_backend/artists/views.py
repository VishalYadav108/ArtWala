from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from .models import ArtistProfile, ArtistReview, ArtistFollowing
from .serializers import (
    ArtistProfileSerializer, 
    ArtistReviewSerializer, 
    ArtistRegistrationSerializer,
    ArtistLoginSerializer,
    ArtistFollowingSerializer
)

class ArtistProfileViewSet(viewsets.ModelViewSet):
    queryset = ArtistProfile.objects.all()
    serializer_class = ArtistProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """
        Get analytics for the current artist (mock data for now)
        """
        # TODO: Implement real analytics calculation
        mock_analytics = {
            'total_sales': 2500.00,
            'total_orders': 12,
            'total_commissions': 5,
            'profile_views': 234,
            'products_sold': 8,
            'average_rating': 4.6
        }
        return Response(mock_analytics)
    
    @action(detail=True, methods=['post'])
    def follow(self, request, slug=None):
        """
        Follow an artist
        """
        artist = self.get_object()
        user = request.user
        
        if artist.user == user:
            return Response(
                {'error': 'You cannot follow yourself'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            following, created = ArtistFollowing.objects.get_or_create(
                follower=user,
                artist=artist
            )
            
            if created:
                return Response(
                    {'message': f'You are now following {artist.display_name}'},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'message': f'You are already following {artist.display_name}'},
                    status=status.HTTP_200_OK
                )
        except IntegrityError:
            return Response(
                {'error': 'Failed to follow artist'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def unfollow(self, request, slug=None):
        """
        Unfollow an artist
        """
        artist = self.get_object()
        user = request.user
        
        try:
            following = ArtistFollowing.objects.get(
                follower=user,
                artist=artist
            )
            following.delete()
            
            return Response(
                {'message': f'You have unfollowed {artist.display_name}'},
                status=status.HTTP_200_OK
            )
        except ArtistFollowing.DoesNotExist:
            return Response(
                {'error': f'You are not following {artist.display_name}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def following(self, request):
        """
        Get all artists the current user is following
        """
        user = request.user
        followings = ArtistFollowing.objects.filter(follower=user)
        serializer = ArtistFollowingSerializer(followings, many=True)
        return Response(serializer.data)

class ArtistReviewViewSet(viewsets.ModelViewSet):
    queryset = ArtistReview.objects.all()
    serializer_class = ArtistReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

class ArtistRegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = ArtistRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            artist = serializer.save()
            user = artist.user
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'user_type': user.user_type,
                },
                'artist': ArtistProfileSerializer(artist).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArtistLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = ArtistLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            artist = user.artist_profile
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'user_type': user.user_type,
                },
                'artist': ArtistProfileSerializer(artist).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArtistFollowingViewSet(viewsets.ModelViewSet):
    serializer_class = ArtistFollowingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filter followings by the current user
        return ArtistFollowing.objects.filter(follower=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)
