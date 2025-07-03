from django.db import models
from django.conf import settings
from artists.models import ArtistProfile

class CommissionRequest(models.Model):
    """
    Custom artwork requests from clients to artists
    Initiates the commission workflow and contains all project requirements
    """
    # Request lifecycle status tracking
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),         # Client has posted the request
        ('under_review', 'Under Review'),   # Artist is considering the request
        ('accepted', 'Accepted'),           # Artist has accepted and proposal created
        ('in_progress', 'In Progress'),     # Work has begun on the commission
        ('completed', 'Completed'),         # Artwork finished, awaiting delivery
        ('delivered', 'Delivered'),         # Client has received final artwork
        ('rejected', 'Rejected'),           # Artist declined the request
        ('cancelled', 'Cancelled'),         # Client cancelled before completion
    ]
    
    # Types of artwork that can be commissioned
    COMMISSION_TYPE_CHOICES = [
        ('painting', 'Painting'),           # Traditional or digital paintings
        ('sculpture', 'Sculpture'),         # 3D artworks and sculptures
        ('mural', 'Mural'),                # Large-scale wall art
        ('portrait', 'Portrait'),           # Personal or pet portraits
        ('digital_art', 'Digital Art'),     # Digital illustrations and graphics
        ('illustration', 'Illustration'),   # Book, magazine, or concept illustrations
        ('other', 'Other'),                # Custom or mixed media projects
    ]
    
    # Core relationships
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='commission_requests',
        help_text="Customer requesting the custom artwork"
    )
    artist = models.ForeignKey(
        ArtistProfile, 
        on_delete=models.CASCADE, 
        related_name='commission_requests',
        help_text="Artist being asked to create the custom work"
    )
    
    # Project details
    title = models.CharField(
        max_length=200,
        help_text="Brief title describing the requested artwork"
    )
    description = models.TextField(
        help_text="Detailed description of what client wants created"
    )
    commission_type = models.CharField(
        max_length=20, 
        choices=COMMISSION_TYPE_CHOICES,
        help_text="Category of artwork being requested"
    )
    
    # Budget and timeline
    budget_min = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Minimum amount client is willing to pay"
    )
    budget_max = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Maximum amount client is willing to pay"
    )
    deadline = models.DateField(
        help_text="When client needs the artwork completed by"
    )
    
    # Specifications and requirements
    dimensions = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Desired size/dimensions of finished artwork"
    )
    reference_images = models.JSONField(
        default=list, 
        blank=True,
        help_text="URLs of reference images to guide the artist"
    )
    additional_requirements = models.TextField(
        blank=True,
        help_text="Any special requirements, materials, or style preferences"
    )
    
    # Status tracking
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='submitted',
        help_text="Current stage of the commission request"
    )
    
    # Timestamp tracking
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When commission request was submitted"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last time request details or status were updated"
    )
    
    def __str__(self):
        return f"{self.title} - {self.client.username} to {self.artist.display_name}"
    
    class Meta:
        db_table = 'commission_requests'
        ordering = ['-created_at']

class CommissionProposal(models.Model):
    """
    Artist's detailed proposal responding to a commission request
    Contains pricing, timeline, and terms offered by the artist
    """
    # Core relationship
    commission_request = models.OneToOneField(
        CommissionRequest, 
        on_delete=models.CASCADE, 
        related_name='proposal',
        help_text="The commission request this proposal responds to"
    )
    
    # Pricing and timeline proposal
    proposed_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Artist's quoted price for completing the commission"
    )
    estimated_completion_time = models.PositiveIntegerField(
        help_text="Estimated days to complete the artwork from start"
    )
    
    # Detailed proposal content
    proposal_description = models.TextField(
        help_text="Artist's interpretation of the request and approach to the work"
    )
    terms_and_conditions = models.TextField(
        help_text="Artist's terms, payment schedule, and project conditions"
    )
    
    # Supporting materials
    sample_images = models.JSONField(
        default=list, 
        blank=True,
        help_text="URLs of artist's previous similar work to demonstrate capability"
    )
    milestone_plan = models.JSONField(
        default=list, 
        blank=True,
        help_text="Breakdown of project stages with timelines and payment percentages"
    )
    
    # Timestamp tracking
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When artist submitted this proposal"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last time proposal was modified"
    )

class CommissionContract(models.Model):
    """
    Finalized agreement between client and artist
    Created when client accepts artist's proposal and both parties commit
    """
    # Core relationship
    commission_request = models.OneToOneField(
        CommissionRequest, 
        on_delete=models.CASCADE, 
        related_name='contract',
        help_text="The commission request this contract formalizes"
    )
    
    # Final agreed terms
    final_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Agreed final price for the commission"
    )
    start_date = models.DateField(
        help_text="When artist will begin work on the commission"
    )
    expected_completion_date = models.DateField(
        help_text="Target completion date agreed by both parties"
    )
    terms_agreed = models.TextField(
        help_text="Final terms and conditions both parties have agreed to"
    )
    
    # Digital signature tracking
    client_signed = models.BooleanField(
        default=False,
        help_text="Whether client has digitally agreed to contract terms"
    )
    artist_signed = models.BooleanField(
        default=False,
        help_text="Whether artist has digitally agreed to contract terms"
    )
    client_signed_at = models.DateTimeField(
        blank=True, 
        null=True,
        help_text="Timestamp when client signed the contract"
    )
    artist_signed_at = models.DateTimeField(
        blank=True, 
        null=True,
        help_text="Timestamp when artist signed the contract"
    )
    
    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When contract was first created"
    )
    
    def __str__(self):
        return f"Contract for {self.commission_request.title}"
    
    class Meta:
        db_table = 'commission_contracts'

class CommissionMilestone(models.Model):
    """
    Project progress tracking milestones for commissions
    Breaks down commission work into manageable stages with deliverables
    """
    # Milestone status options
    STATUS_CHOICES = [
        ('pending', 'Pending'),         # Not yet started
        ('in_progress', 'In Progress'), # Currently being worked on
        ('completed', 'Completed'),     # Finished and submitted
        ('approved', 'Approved'),       # Client has approved this stage
        ('revision_requested', 'Revision Requested'), # Client requested changes
    ]
    
    # Core relationships
    commission_request = models.ForeignKey(
        CommissionRequest, 
        on_delete=models.CASCADE, 
        related_name='milestones',
        help_text="The commission this milestone belongs to"
    )
    
    # Milestone details
    title = models.CharField(
        max_length=200,
        help_text="Name of this milestone (e.g., 'Initial Sketch', 'Color Study')"
    )
    description = models.TextField(
        help_text="Detailed description of what will be delivered at this stage"
    )
    order = models.PositiveIntegerField(
        help_text="Sequence order of this milestone in the project (1, 2, 3...)"
    )
    percentage = models.PositiveIntegerField(
        help_text="Percentage of total work completed at this milestone"
    )
    payment_percentage = models.PositiveIntegerField(
        help_text="Percentage of total payment released upon milestone completion"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        help_text="Current status of this milestone"
    )
    
    # Progress documentation
    progress_images = models.JSONField(
        default=list, 
        blank=True,
        help_text="URLs of work-in-progress images for this milestone"
    )
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
