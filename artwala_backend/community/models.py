from django.db import models
from django.conf import settings

class Forum(models.Model):
    """
    Community discussion forums organized by topic or theme
    Provides structured spaces for different types of conversations
    """
    # Basic forum information
    name = models.CharField(
        max_length=100,
        help_text="Display name of the forum (e.g., 'General Discussion', 'Technique Tips')"
    )
    slug = models.SlugField(
        unique=True,
        help_text="URL-friendly version of forum name"
    )
    description = models.TextField(
        help_text="Description of forum purpose and guidelines"
    )
    
    # Access control
    is_private = models.BooleanField(
        default=False,
        help_text="Whether forum is restricted to certain user groups"
    )
    
    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this forum was created"
    )

class ForumPost(models.Model):
    """
    Individual discussion threads within forums
    Contains the main content that users can comment on and engage with
    """
    # Post categorization for better organization
    POST_TYPE_CHOICES = [
        ('discussion', 'Discussion'),      # General conversations
        ('job', 'Job Posting'),           # Career opportunities
        ('collaboration', 'Collaboration'), # Project partnerships
        ('help', 'Help/Question'),        # Seeking assistance
        ('showcase', 'Showcase'),         # Displaying artwork or achievements
    ]
    
    # Core relationships
    forum = models.ForeignKey(
        Forum, 
        on_delete=models.CASCADE, 
        related_name='posts',
        help_text="Forum this post belongs to"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        help_text="User who created this post"
    )
    
    # Post content and metadata
    title = models.CharField(
        max_length=200,
        help_text="Post headline/subject line"
    )
    slug = models.SlugField(
        max_length=250,
        help_text="URL-friendly version of post title"
    )
    content = models.TextField(
        help_text="Main body text of the post"
    )
    post_type = models.CharField(
        max_length=20, 
        choices=POST_TYPE_CHOICES, 
        default='discussion',
        help_text="Category of post for filtering and organization"
    )
    
    # Enhanced content features
    tags = models.JSONField(
        default=list, 
        blank=True,
        help_text="Searchable keywords related to post content"
    )
    images = models.JSONField(
        default=list, 
        blank=True,
        help_text="URLs of images attached to this post"
    )
    
    # Moderation and visibility controls
    is_pinned = models.BooleanField(
        default=False,
        help_text="Whether post stays at top of forum (important announcements)"
    )
    is_locked = models.BooleanField(
        default=False,
        help_text="Whether new comments are disabled on this post"
    )
    
    # Engagement metrics
    views_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of times this post has been viewed"
    )
    likes_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of users who have liked this post"
    )
    
    # Timestamp tracking
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When post was originally created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last time post content was edited"
    )
    
    def __str__(self):
        return f"{self.title} by {self.author.username}"
    
    class Meta:
        db_table = 'forum_posts'
        ordering = ['-created_at']

class ForumComment(models.Model):
    """
    User responses and discussions on forum posts
    Supports threaded conversations with reply functionality
    """
    # Core relationships
    post = models.ForeignKey(
        ForumPost, 
        on_delete=models.CASCADE, 
        related_name='comments',
        help_text="The forum post this comment belongs to"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        help_text="User who wrote this comment"
    )
    
    # Comment content
    content = models.TextField(
        help_text="The actual comment text"
    )
    
    # Threading support for nested replies
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='replies',
        help_text="Parent comment if this is a reply (null for top-level comments)"
    )
    
    # Engagement tracking
    likes_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of users who have liked this comment"
    )
    
    # Timestamp tracking
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When comment was posted"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last time comment was edited"
    )

class PostLike(models.Model):
    """
    User likes/favorites on forum posts
    Tracks engagement and popular content
    """
    # Relationship fields
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        help_text="User who liked the post"
    )
    post = models.ForeignKey(
        ForumPost, 
        on_delete=models.CASCADE, 
        related_name='likes',
        help_text="Post that was liked"
    )
    
    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the like was created"
    )

class CommentLike(models.Model):
    """
    User likes on individual comments
    Enables community feedback on comment quality
    """
    # Relationship fields
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        help_text="User who liked the comment"
    )
    comment = models.ForeignKey(
        ForumComment, 
        on_delete=models.CASCADE, 
        related_name='likes',
        help_text="Comment that was liked"
    )
    
    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the like was created"
    )

class JobPosting(models.Model):
    """
    Art-related job opportunities posted by community members
    Connects artists with employment and freelance opportunities
    """
    # Employment type categorization
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),     # Permanent full-time positions
        ('part_time', 'Part Time'),     # Regular part-time work
        ('freelance', 'Freelance'),     # Project-based independent work
        ('contract', 'Contract'),       # Fixed-term contract positions
        ('internship', 'Internship'),   # Learning and training opportunities
    ]
    
    # Core job information
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='job_postings',
        help_text="User/company who posted this job opportunity"
    )
    title = models.CharField(
        max_length=200,
        help_text="Job title/position name"
    )
    slug = models.SlugField(
        max_length=250,
        help_text="URL-friendly version of job title"
    )
    description = models.TextField(
        help_text="Detailed job description, responsibilities, and role overview"
    )
    
    # Employer information
    company = models.CharField(
        max_length=100,
        help_text="Name of hiring company or organization"
    )
    location = models.CharField(
        max_length=100,
        help_text="Job location (city, remote, etc.)"
    )
    
    # Job details
    job_type = models.CharField(
        max_length=20, 
        choices=JOB_TYPE_CHOICES,
        help_text="Type of employment being offered"
    )
    salary_range = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Compensation range (optional, e.g., '$50k-70k', 'Competitive')"
    )
    requirements = models.TextField(
        help_text="Required skills, experience, and qualifications"
    )
    
    # Application details
    application_deadline = models.DateField(
        blank=True, 
        null=True,
        help_text="Last date to apply for this position"
    )
    contact_email = models.EmailField(
        help_text="Email address for job applications and inquiries"
    )
    
    # Status and management
    is_active = models.BooleanField(
        default=True,
        help_text="Whether job is still accepting applications"
    )
    
    # Timestamp tracking
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When job was posted"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last time job details were modified"
    )
    
    def __str__(self):
        return f"{self.title} at {self.company}"
    
    class Meta:
        db_table = 'job_postings'
        ordering = ['-created_at']
