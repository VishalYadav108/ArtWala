from django.db import models
from django.conf import settings
from django.utils.text import slugify

class ArtistProfile(models.Model):
    """
    Artist profile extending the User model
    Contains professional information, portfolio data, and business settings for artists
    """
    # Core relationship and identification
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='artist_profile',
        help_text="Links to the base User account for this artist"
    )
    slug = models.SlugField(
        unique=True, 
        max_length=100,
        help_text="URL-friendly version of artist name for profile URLs"
    )
    
    # Public display information
    display_name = models.CharField(
        max_length=100,
        help_text="Artist's professional name shown publicly"
    )
    tagline = models.CharField(
        max_length=200, 
        blank=True,
        help_text="Short catchphrase or description under artist name"
    )
    logo = models.ImageField(
        upload_to='artist_logos/', 
        blank=True, 
        null=True,
        help_text="Artist's brand logo or signature artwork"
    )
    
    # Portfolio and work showcase
    portfolio_images = models.JSONField(
        default=list, 
        blank=True,
        help_text="Array of portfolio image URLs showcasing artist's work"
    )
    specializations = models.JSONField(
        default=list, 
        blank=True,
        help_text="List of art mediums/styles artist specializes in (painting, sculpture, etc.)"
    )
    
    # Professional background
    experience_years = models.PositiveIntegerField(
        default=0,
        help_text="Number of years artist has been practicing professionally"
    )
    education = models.TextField(
        blank=True,
        help_text="Educational background and art-related qualifications"
    )
    awards = models.TextField(
        blank=True,
        help_text="Notable awards, exhibitions, and recognitions"
    )
    artist_statement = models.TextField(
        blank=True,
        help_text="Personal artistic philosophy and approach description"
    )
    
    # Commission and business settings
    commission_available = models.BooleanField(
        default=True,
        help_text="Whether artist is currently accepting commission requests"
    )
    commission_price_range = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Typical price range for commissioned work (e.g., '$500-$2000')"
    )
    response_time = models.CharField(
        max_length=50, 
        default='24 hours',
        help_text="How quickly artist typically responds to inquiries"
    )
    
    # Platform status and metrics
    featured = models.BooleanField(
        default=False,
        help_text="Whether artist is featured prominently on platform"
    )
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.0,
        help_text="Average customer rating (0.00 to 5.00)"
    )
    total_reviews = models.PositiveIntegerField(
        default=0,
        help_text="Total number of reviews received from customers"
    )
    
    # Timestamp tracking
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When artist profile was first created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last time profile information was modified"
    )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.display_name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.display_name} - {self.user.email}"
    
    class Meta:
        db_table = 'artist_profiles'
        verbose_name = 'Artist Profile'
        verbose_name_plural = 'Artist Profiles'

class ArtistReview(models.Model):
    """
    Customer reviews and ratings for artists
    Enables feedback system for artist quality and service evaluation
    """
    # Relationship fields
    artist = models.ForeignKey(
        ArtistProfile, 
        on_delete=models.CASCADE, 
        related_name='reviews',
        help_text="The artist being reviewed"
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        help_text="User who wrote this review (must be a customer)"
    )
    
    # Review content
    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        help_text="Star rating from 1 (poor) to 5 (excellent)"
    )
    comment = models.TextField(
        help_text="Written review describing the customer's experience"
    )
    
    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this review was submitted"
    )
    
    class Meta:
        db_table = 'artist_reviews'
        unique_together = ['artist', 'reviewer']
        verbose_name = 'Artist Review'
        verbose_name_plural = 'Artist Reviews'
