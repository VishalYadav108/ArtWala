from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Chapter, ChapterEvent, ChapterMembership, EventRegistration
from .serializers import ChapterSerializer, ChapterEventSerializer, ChapterMembershipSerializer, EventRegistrationSerializer
from artists.models import ArtistProfile

class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def join(self, request, slug=None):
        chapter = self.get_object()
        user = request.user
        
        # Check if the user has an artist profile
        try:
            artist_profile = ArtistProfile.objects.get(user=user)
        except ArtistProfile.DoesNotExist:
            return Response({"detail": "You need an artist profile to join a chapter."}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Check if artist is already a member
        if ChapterMembership.objects.filter(artist=artist_profile, chapter=chapter, is_active=True).exists():
            return Response({"detail": "You are already a member of this chapter."}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Create or reactivate membership
        membership, created = ChapterMembership.objects.get_or_create(
            artist=artist_profile,
            chapter=chapter,
            defaults={'is_active': True}
        )
        
        if not created:
            membership.is_active = True
            membership.save()
            
        serializer = ChapterMembershipSerializer(membership)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def leave(self, request, slug=None):
        chapter = self.get_object()
        user = request.user
        
        try:
            artist_profile = ArtistProfile.objects.get(user=user)
        except ArtistProfile.DoesNotExist:
            return Response({"detail": "You don't have an artist profile."}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        try:
            membership = ChapterMembership.objects.get(
                artist=artist_profile, 
                chapter=chapter,
                is_active=True
            )
            membership.is_active = False
            membership.save()
            return Response({"detail": "You have left the chapter."}, 
                           status=status.HTTP_200_OK)
        except ChapterMembership.DoesNotExist:
            return Response({"detail": "You are not an active member of this chapter."}, 
                           status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def members(self, request, slug=None):
        chapter = self.get_object()
        memberships = ChapterMembership.objects.filter(chapter=chapter, is_active=True)
        serializer = ChapterMembershipSerializer(memberships, many=True)
        return Response(serializer.data)

class ChapterEventViewSet(viewsets.ModelViewSet):
    queryset = ChapterEvent.objects.all()
    serializer_class = ChapterEventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def register(self, request, slug=None):
        event = self.get_object()
        user = request.user
        
        # Check if registration is already made
        if EventRegistration.objects.filter(event=event, user=user).exists():
            return Response({"detail": "You are already registered for this event."}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Check if event has reached capacity
        if event.max_participants and event.registrations.count() >= event.max_participants:
            return Response({"detail": "This event has reached its maximum capacity."}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Create registration
        registration = EventRegistration.objects.create(event=event, user=user)
        serializer = EventRegistrationSerializer(registration)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel_registration(self, request, slug=None):
        event = self.get_object()
        user = request.user
        
        try:
            registration = EventRegistration.objects.get(event=event, user=user)
            registration.delete()
            return Response({"detail": "Your registration has been cancelled."}, 
                           status=status.HTTP_200_OK)
        except EventRegistration.DoesNotExist:
            return Response({"detail": "You are not registered for this event."}, 
                           status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def registrations(self, request, slug=None):
        event = self.get_object()
        
        # Only allow chapter admins or event creator to see registrations
        if not (request.user.is_staff or 
                request.user == event.created_by or 
                request.user == event.chapter.admin):
            return Response({"detail": "You don't have permission to view registrations."}, 
                           status=status.HTTP_403_FORBIDDEN)
        
        registrations = EventRegistration.objects.filter(event=event)
        serializer = EventRegistrationSerializer(registrations, many=True)
        return Response(serializer.data)

class ChapterMembershipViewSet(viewsets.ModelViewSet):
    queryset = ChapterMembership.objects.all()
    serializer_class = ChapterMembershipSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter memberships to show only the current user's artist memberships"""
        user = self.request.user
        
        # For staff/admin, show all memberships
        if user.is_staff:
            return ChapterMembership.objects.all()
            
        # For regular users, only show their own memberships
        try:
            artist_profile = ArtistProfile.objects.get(user=user)
            return ChapterMembership.objects.filter(artist=artist_profile)
        except ArtistProfile.DoesNotExist:
            return ChapterMembership.objects.none()

class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter registrations to show only the current user's registrations"""
        user = self.request.user
        
        # For staff/admin, show all registrations
        if user.is_staff:
            return EventRegistration.objects.all()
            
        # For regular users, only show their own registrations
        return EventRegistration.objects.filter(user=user)
