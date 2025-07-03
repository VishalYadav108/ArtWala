from django.db import models
from django.conf import settings
from artists.models import ArtistProfile

class Chapter(models.Model):
    """
    City-based art communities and chapters
    Organizes artists by geographic location for local networking and events
    """
    # Basic chapter information
    name = models.CharField(
        max_length=100,
        help_text="Display name of the chapter (e.g., 'Mumbai Chapter', 'Delhi Art Community')"
    )
    slug = models.SlugField(
        unique=True,
        help_text="URL-friendly version of chapter name for web addresses"
    )
    
    # Geographic location
    city = models.CharField(
        max_length=100,
        help_text="Primary city this chapter serves"
    )
    state = models.CharField(
        max_length=100,
        help_text="State or province where chapter is located"
    )
    country = models.CharField(
        max_length=100, 
        default='India',
        help_text="Country where chapter operates"
    )
    
    # Chapter details and presentation
    description = models.TextField(
        help_text="Detailed description of chapter's mission, activities, and community"
    )
    cover_image = models.ImageField(
        upload_to='chapter_images/', 
        blank=True, 
        null=True,
        help_text="Header image representing the chapter and local art scene"
    )
    
    # Management and administration
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='managed_chapters',
        help_text="User responsible for managing this chapter"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether chapter is currently operational and accepting members"
    )
    
    # Contact information
    contact_email = models.EmailField(
        blank=True,
        help_text="Public email for chapter inquiries and communication"
    )
    contact_phone = models.CharField(
        max_length=15, 
        blank=True,
        help_text="Optional phone number for chapter contact"
    )
    social_links = models.JSONField(
        default=dict, 
        blank=True,
        help_text="Chapter's social media profiles and websites"
    )
    
    # Timestamp tracking
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this chapter was established on the platform"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last time chapter information was modified"
    )
    
    def __str__(self):
        return f"{self.name} - {self.city}"
    
    class Meta:
        db_table = 'chapters'
        verbose_name = 'Chapter'
        verbose_name_plural = 'Chapters'

class ChapterMembership(models.Model):
    """
    Artist membership in local chapters
    Tracks which artists belong to which geographic communities
    """
    # Relationship fields
    chapter = models.ForeignKey(
        Chapter, 
        on_delete=models.CASCADE, 
        related_name='memberships',
        help_text="The chapter this membership belongs to"
    )
    artist = models.ForeignKey(
        ArtistProfile, 
        on_delete=models.CASCADE, 
        related_name='chapter_memberships',
        help_text="The artist who is a member of this chapter"
    )
    
    # Membership details
    joined_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When artist joined this chapter"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether membership is currently active (not suspended or left)"
    )

class ChapterEvent(models.Model):
    """
    Events organized by local chapters
    Includes exhibitions, workshops, meetups, and competitions
    """
    # Event categorization
    EVENT_TYPE_CHOICES = [
        ('exhibition', 'Exhibition'),   # Art shows and gallery events
        ('workshop', 'Workshop'),       # Educational and skill-building sessions
        ('meetup', 'Meetup'),          # Casual networking and social events
        ('competition', 'Competition'), # Contests and challenges
        ('other', 'Other'),            # Miscellaneous event types
    ]
    
    # Core event information
    chapter = models.ForeignKey(
        Chapter, 
        on_delete=models.CASCADE, 
        related_name='events',
        help_text="Chapter organizing this event"
    )
    title = models.CharField(
        max_length=200,
        help_text="Event name/title"
    )
    slug = models.SlugField(
        max_length=250,
        help_text="URL-friendly version of event title"
    )
    description = models.TextField(
        help_text="Detailed event description, agenda, and requirements"
    )
    event_type = models.CharField(
        max_length=20, 
        choices=EVENT_TYPE_CHOICES,
        help_text="Category of event for filtering and organization"
    )
    
    # Scheduling information
    start_date = models.DateTimeField(
        help_text="Event start date and time"
    )
    end_date = models.DateTimeField(
        help_text="Event end date and time"
    )
    location = models.CharField(
        max_length=200,
        help_text="Physical address or venue where event takes place"
    )
    
    # Capacity and pricing
    max_participants = models.PositiveIntegerField(
        blank=True, 
        null=True,
        help_text="Maximum number of attendees (null for unlimited)"
    )
    registration_fee = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        default=0,
        help_text="Cost to attend event (0 for free events)"
    )
    
    # Event presentation
    image = models.ImageField(
        upload_to='event_images/', 
        blank=True, 
        null=True,
        help_text="Event poster or promotional image"
    )
    is_public = models.BooleanField(
        default=True,
        help_text="Whether event is open to all users or chapter members only"
    )
    
    # Event management
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        help_text="User who created/organized this event"
    )
    
    # Timestamp tracking
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When event was first created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last time event details were modified"
    )
    
    def __str__(self):
        return f"{self.title} - {self.chapter.name}"
    
    class Meta:
        db_table = 'chapter_events'
        unique_together = ['chapter', 'slug']

class EventRegistration(models.Model):
    """
    User registrations for chapter events
    Tracks who has signed up for which events and attendance
    """
    # Relationship fields
    event = models.ForeignKey(
        ChapterEvent, 
        on_delete=models.CASCADE, 
        related_name='registrations',
        help_text="The event this registration is for"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        help_text="User who registered for this event"
    )
    
    # Registration details
    registered_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When user registered for the event"
    )
    attended = models.BooleanField(
        default=False,
        help_text="Whether user actually attended the event (updated post-event)"
    )
