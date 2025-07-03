from django.db import models
from django.conf import settings
from django.utils.text import slugify

class ArtistProfile(models.Model):
    """
    Artist profile extending the User model
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='artist_profile')
    slug = models.SlugField(unique=True, max_length=100)
    display_name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200, blank=True)
    logo = models.ImageField(upload_to='artist_logos/', blank=True, null=True)
    portfolio_images = models.JSONField(default=list, blank=True)
    specializations = models.JSONField(default=list, blank=True)  # ["painting", "sculpture", etc.]
    experience_years = models.PositiveIntegerField(default=0)
    education = models.TextField(blank=True)
    awards = models.TextField(blank=True)
    artist_statement = models.TextField(blank=True)
    commission_available = models.BooleanField(default=True)
    commission_price_range = models.CharField(max_length=100, blank=True)
    response_time = models.CharField(max_length=50, default='24 hours')
    featured = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_reviews = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
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
    Reviews for artists
    """
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'artist_reviews'
        unique_together = ['artist', 'reviewer']
        verbose_name = 'Artist Review'
        verbose_name_plural = 'Artist Reviews'
