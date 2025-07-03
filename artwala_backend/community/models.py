from django.db import models
from django.conf import settings

class Forum(models.Model):
    """
    Community forums
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'forums'

class ForumPost(models.Model):
    """
    Forum posts
    """
    POST_TYPE_CHOICES = [
        ('discussion', 'Discussion'),
        ('job', 'Job Posting'),
        ('collaboration', 'Collaboration'),
        ('help', 'Help/Question'),
        ('showcase', 'Showcase'),
    ]
    
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    content = models.TextField()
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default='discussion')
    tags = models.JSONField(default=list, blank=True)
    images = models.JSONField(default=list, blank=True)
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} by {self.author.username}"
    
    class Meta:
        db_table = 'forum_posts'
        ordering = ['-created_at']

class ForumComment(models.Model):
    """
    Comments on forum posts
    """
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    likes_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'forum_comments'
        ordering = ['created_at']

class PostLike(models.Model):
    """
    Likes on forum posts
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'post_likes'
        unique_together = ['user', 'post']

class CommentLike(models.Model):
    """
    Likes on forum comments
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(ForumComment, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'comment_likes'
        unique_together = ['user', 'comment']

class JobPosting(models.Model):
    """
    Job postings in community
    """
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('freelance', 'Freelance'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]
    
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_postings')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    description = models.TextField()
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    salary_range = models.CharField(max_length=100, blank=True)
    requirements = models.TextField()
    application_deadline = models.DateField(blank=True, null=True)
    contact_email = models.EmailField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} at {self.company}"
    
    class Meta:
        db_table = 'job_postings'
        ordering = ['-created_at']
