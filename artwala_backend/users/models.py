from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    Handles user authentication, profile information, and user categorization
    """
    # User type classification for role-based functionality
    USER_TYPE_CHOICES = [
        ('artist', 'Artist'),    # Users who sell artwork and offer commissions
        ('buyer', 'Buyer'),      # Users who purchase artwork and request commissions
        ('admin', 'Admin'),      # Platform administrators with full access
    ]
    
    # Primary identification and authentication fields
    email = models.EmailField(unique=True)  # Primary login credential, must be unique
    user_type = models.CharField(
        max_length=20, 
        choices=USER_TYPE_CHOICES, 
        default='buyer',
        help_text="Defines user role and available features"
    )
    
    # Contact and personal information
    phone = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        help_text="Optional phone number for account verification and communication"
    )
    
    # Profile presentation fields
    profile_image = models.ImageField(
        upload_to='profile_images/', 
        blank=True, 
        null=True,
        help_text="User's profile picture displayed throughout the platform"
    )
    bio = models.TextField(
        blank=True,
        help_text="Personal description or artist statement for public profile"
    )
    location = models.CharField(
        max_length=100, 
        blank=True,
        help_text="User's city/location for local chapter assignment and shipping"
    )
    
    # External links and social presence
    website = models.URLField(
        blank=True,
        help_text="Personal or professional website URL"
    )
    social_links = models.JSONField(
        default=dict, 
        blank=True,
        help_text="Social media profiles stored as JSON (Instagram, Twitter, etc.)"
    )
    
    # Account status and verification
    is_verified = models.BooleanField(
        default=False,
        help_text="Indicates if user's identity has been verified by platform"
    )
    
    # Timestamp tracking for audit and analytics
    date_joined = models.DateTimeField(
        auto_now_add=True,
        help_text="Account creation timestamp"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last profile update timestamp"
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    def __str__(self):
        return f"{self.email} ({self.user_type})"
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
