from django.db import models
from django.conf import settings
from artists.models import ArtistProfile

class Chapter(models.Model):
    """
    City-based chapters
    """
    name = models.CharField(max_length=100)  # "Mumbai Chapter"
    slug = models.SlugField(unique=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India')
    description = models.TextField()
    cover_image = models.ImageField(upload_to='chapter_images/', blank=True, null=True)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='managed_chapters')
    is_active = models.BooleanField(default=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=15, blank=True)
    social_links = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.city}"
    
    class Meta:
        db_table = 'chapters'
        verbose_name = 'Chapter'
        verbose_name_plural = 'Chapters'

class ChapterMembership(models.Model):
    """
    Artist membership in chapters
    """
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='memberships')
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE, related_name='chapter_memberships')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'chapter_memberships'
        unique_together = ['chapter', 'artist']

class ChapterEvent(models.Model):
    """
    Chapter events
    """
    EVENT_TYPE_CHOICES = [
        ('exhibition', 'Exhibition'),
        ('workshop', 'Workshop'),
        ('meetup', 'Meetup'),
        ('competition', 'Competition'),
        ('other', 'Other'),
    ]
    
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    max_participants = models.PositiveIntegerField(blank=True, null=True)
    registration_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    is_public = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.chapter.name}"
    
    class Meta:
        db_table = 'chapter_events'
        unique_together = ['chapter', 'slug']

class EventRegistration(models.Model):
    """
    Event registrations
    """
    event = models.ForeignKey(ChapterEvent, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'event_registrations'
        unique_together = ['event', 'user']
