from django.db import models
from django.conf import settings
from artists.models import ArtistProfile

class CommissionRequest(models.Model):
    """
    Commission requests from buyers to artists
    """
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('delivered', 'Delivered'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    COMMISSION_TYPE_CHOICES = [
        ('painting', 'Painting'),
        ('sculpture', 'Sculpture'),
        ('mural', 'Mural'),
        ('portrait', 'Portrait'),
        ('digital_art', 'Digital Art'),
        ('illustration', 'Illustration'),
        ('other', 'Other'),
    ]
    
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='commission_requests')
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE, related_name='commission_requests')
    title = models.CharField(max_length=200)
    description = models.TextField()
    commission_type = models.CharField(max_length=20, choices=COMMISSION_TYPE_CHOICES)
    budget_min = models.DecimalField(max_digits=10, decimal_places=2)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    dimensions = models.CharField(max_length=100, blank=True)
    reference_images = models.JSONField(default=list, blank=True)
    additional_requirements = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.client.username} to {self.artist.display_name}"
    
    class Meta:
        db_table = 'commission_requests'
        ordering = ['-created_at']

class CommissionProposal(models.Model):
    """
    Artist's proposal for a commission request
    """
    commission_request = models.OneToOneField(CommissionRequest, on_delete=models.CASCADE, related_name='proposal')
    proposed_price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_completion_time = models.PositiveIntegerField(help_text="Estimated days to complete")
    proposal_description = models.TextField()
    terms_and_conditions = models.TextField()
    sample_images = models.JSONField(default=list, blank=True)
    milestone_plan = models.JSONField(default=list, blank=True)  # [{"stage": "sketch", "days": 3, "payment": 25}]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Proposal for {self.commission_request.title}"
    
    class Meta:
        db_table = 'commission_proposals'

class CommissionContract(models.Model):
    """
    Finalized commission contract
    """
    commission_request = models.OneToOneField(CommissionRequest, on_delete=models.CASCADE, related_name='contract')
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    expected_completion_date = models.DateField()
    terms_agreed = models.TextField()
    client_signed = models.BooleanField(default=False)
    artist_signed = models.BooleanField(default=False)
    client_signed_at = models.DateTimeField(blank=True, null=True)
    artist_signed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Contract for {self.commission_request.title}"
    
    class Meta:
        db_table = 'commission_contracts'

class CommissionMilestone(models.Model):
    """
    Commission milestones/progress tracking
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('approved', 'Approved'),
        ('revision_requested', 'Revision Requested'),
    ]
    
    commission_request = models.ForeignKey(CommissionRequest, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField()
    percentage = models.PositiveIntegerField(help_text="Percentage of total work")
    payment_percentage = models.PositiveIntegerField(help_text="Percentage of total payment")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    progress_images = models.JSONField(default=list, blank=True)
    client_feedback = models.TextField(blank=True)
    due_date = models.DateField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'commission_milestones'
        ordering = ['order']

class CommissionPayment(models.Model):
    """
    Commission payments
    """
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    commission_request = models.ForeignKey(CommissionRequest, on_delete=models.CASCADE, related_name='payments')
    milestone = models.ForeignKey(CommissionMilestone, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'commission_payments'
        ordering = ['-created_at']

class CommissionReview(models.Model):
    """
    Reviews for completed commissions
    """
    commission_request = models.OneToOneField(CommissionRequest, on_delete=models.CASCADE, related_name='review')
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    would_recommend = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'commission_reviews'
