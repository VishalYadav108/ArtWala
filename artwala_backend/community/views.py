from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Forum, ForumPost, JobPosting
from .serializers import ForumSerializer, ForumPostSerializer

class ForumViewSet(viewsets.ModelViewSet):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

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
