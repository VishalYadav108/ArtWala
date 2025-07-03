from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Chapter, ChapterEvent, ChapterMembership
from .serializers import ChapterSerializer, ChapterEventSerializer, ChapterMembershipSerializer

class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class ChapterEventViewSet(viewsets.ModelViewSet):
    queryset = ChapterEvent.objects.all()
    serializer_class = ChapterEventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class ChapterMembershipViewSet(viewsets.ModelViewSet):
    queryset = ChapterMembership.objects.all()
    serializer_class = ChapterMembershipSerializer
    permission_classes = [IsAuthenticated]
