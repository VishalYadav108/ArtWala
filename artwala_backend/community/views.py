from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Forum, ForumPost, JobPosting, ForumMembership
from .serializers import ForumSerializer, ForumPostSerializer, ForumMembershipSerializer

class ForumViewSet(viewsets.ModelViewSet):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def join(self, request, slug=None):
        forum = self.get_object()
        user = request.user
        
        # Check if user is already a member
        if ForumMembership.objects.filter(user=user, forum=forum).exists():
            return Response({"detail": "You are already a member of this forum."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Create membership
        membership = ForumMembership.objects.create(user=user, forum=forum)
        serializer = ForumMembershipSerializer(membership)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def leave(self, request, slug=None):
        forum = self.get_object()
        user = request.user
        
        # Check if user is a member
        try:
            membership = ForumMembership.objects.get(user=user, forum=forum)
            membership.delete()
            return Response({"detail": "You have left the forum."}, 
                            status=status.HTTP_200_OK)
        except ForumMembership.DoesNotExist:
            return Response({"detail": "You are not a member of this forum."}, 
                            status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def members(self, request, slug=None):
        forum = self.get_object()
        memberships = ForumMembership.objects.filter(forum=forum)
        serializer = ForumMembershipSerializer(memberships, many=True)
        return Response(serializer.data)

class ForumMembershipViewSet(viewsets.ModelViewSet):
    queryset = ForumMembership.objects.all()
    serializer_class = ForumMembershipSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter memberships to show only user's memberships"""
        user = self.request.user
        return ForumMembership.objects.filter(user=user)
    
    def perform_create(self, serializer):
        """Set the user to the current logged-in user when creating a membership"""
        serializer.save(user=self.request.user)

class ForumPostViewSet(viewsets.ModelViewSet):
    queryset = ForumPost.objects.all()
    serializer_class = ForumPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

# Alias for posts endpoint
class PostViewSet(ForumPostViewSet):
    pass

class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
