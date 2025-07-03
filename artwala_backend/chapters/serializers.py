from rest_framework import serializers
from .models import Chapter, ChapterMembership, ChapterEvent, EventRegistration

class ChapterSerializer(serializers.ModelSerializer):
    admin_name = serializers.CharField(source='admin.get_full_name', read_only=True)
    members_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Chapter
        fields = '__all__'
    
    def get_members_count(self, obj):
        return obj.memberships.filter(is_active=True).count()

class ChapterMembershipSerializer(serializers.ModelSerializer):
    chapter_name = serializers.CharField(source='chapter.name', read_only=True)
    artist_name = serializers.CharField(source='artist.display_name', read_only=True)
    
    class Meta:
        model = ChapterMembership
        fields = '__all__'

class ChapterEventSerializer(serializers.ModelSerializer):
    chapter_name = serializers.CharField(source='chapter.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    registrations_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ChapterEvent
        fields = '__all__'
    
    def get_registrations_count(self, obj):
        return obj.registrations.count()

class EventRegistrationSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = EventRegistration
        fields = '__all__'
