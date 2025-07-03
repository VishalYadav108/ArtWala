from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import ArtistProfile, ArtistReview
from .serializers import ArtistProfileSerializer, ArtistReviewSerializer

class ArtistProfileViewSet(viewsets.ModelViewSet):
    queryset = ArtistProfile.objects.all()
    serializer_class = ArtistProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class ArtistReviewViewSet(viewsets.ModelViewSet):
    queryset = ArtistReview.objects.all()
    serializer_class = ArtistReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
