from django.db import models
from django.conf import settings
from artists.models import ArtistProfile

class Category(models.Model):
    """
    Product categories for organizing artworks by type, medium, or style
    Supports hierarchical categorization with parent-child relationships
    """
    # Core category information
    name = models.CharField(
        max_length=100, 
        unique=True,
        help_text="Display name of the category (e.g., 'Paintings', 'Sculptures')"
    )
    slug = models.SlugField(
        unique=True,
        help_text="URL-friendly version of category name for web addresses"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description of what this category includes"
    )
    
    # Visual representation
    image = models.ImageField(
        upload_to='category_images/', 
        blank=True, 
        null=True,
        help_text="Representative image displayed for this category"
    )
    
    # Hierarchical structure
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='subcategories',
        help_text="Parent category for creating nested category structures"
    )
    
    # Status and metadata
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this category is visible and usable on the platform"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this category was first created"
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Product(models.Model):
    """
    Individual artworks and products listed by artists for sale
    Contains all information needed for marketplace display and purchase
    """
    # Publication status options
    STATUS_CHOICES = [
        ('draft', 'Draft'),         # Not yet published, only visible to artist
        ('published', 'Published'), # Live on marketplace, available for purchase
        ('sold', 'Sold'),          # No longer available, marked as sold
        ('archived', 'Archived'),   # Hidden from public but kept for records
    ]
    
    # Core relationships
    artist = models.ForeignKey(
        ArtistProfile, 
        on_delete=models.CASCADE, 
        related_name='products',
        help_text="The artist who created and is selling this artwork"
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products',
        help_text="Primary category this artwork belongs to"
    )
    
    # Basic product information
    title = models.CharField(
        max_length=200,
        help_text="Name/title of the artwork"
    )
    slug = models.SlugField(
        max_length=250,
        help_text="URL-friendly version of title for product pages"
    )
    description = models.TextField(
        help_text="Detailed description of the artwork, inspiration, and techniques"
    )
    tags = models.JSONField(
        default=list, 
        blank=True,
        help_text="Searchable keywords related to the artwork (style, theme, etc.)"
    )
    
    # Pricing and commercial details
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Selling price in platform currency"
    )
    
    # Physical artwork specifications
    dimensions = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Physical size of artwork (e.g., '30x40 inches', '76x102 cm')"
    )
    medium = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Materials and techniques used (e.g., 'Oil on canvas', 'Digital print')"
    )
    year_created = models.PositiveIntegerField(
        blank=True, 
        null=True,
        help_text="Year the artwork was completed"
    )
    is_original = models.BooleanField(
        default=True,
        help_text="Whether this is an original artwork or a reproduction"
    )
    is_framed = models.BooleanField(
        default=False,
        help_text="Whether the artwork comes with a frame"
    )
    weight = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        blank=True, 
        null=True,
        help_text="Weight for shipping calculations (in kg or lbs)"
    )
    
    # Platform management
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft',
        help_text="Current publication status of the product"
    )
    featured = models.BooleanField(
        default=False,
        help_text="Whether to highlight this product prominently on the platform"
    )
    
    # Engagement metrics
    views_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of times this product page has been viewed"
    )
    likes_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of users who have liked/favorited this artwork"
    )
    
    # Timestamp tracking
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this product was first created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last time product information was modified"
    )
    
    def __str__(self):
        return f"{self.title} by {self.artist.display_name}"
    
    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        unique_together = ['artist', 'slug']

class ProductImage(models.Model):
    """
    Multiple images for each product/artwork
    Allows artists to show different angles, details, and contexts
    """
    # Core relationship
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='images',
        help_text="The product this image belongs to"
    )
    
    # Image data and metadata
    image = models.ImageField(
        upload_to='product_images/',
        help_text="The actual image file stored on server or CDN"
    )
    alt_text = models.CharField(
        max_length=200, 
        blank=True,
        help_text="Alternative text for accessibility and SEO"
    )
    
    # Display settings
    is_primary = models.BooleanField(
        default=False,
        help_text="Whether this is the main image shown in listings"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order for image galleries (lower numbers shown first)"
    )

class ProductLike(models.Model):
    """
    User favorites/wishlist functionality for products
    Tracks which users have liked which artworks
    """
    # Relationship fields
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        help_text="User who liked this product"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='likes',
        help_text="Product that was liked"
    )
    
    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this like was created (for activity tracking)"
    )

class Cart(models.Model):
    """
    Shopping cart container for each user
    Holds items before checkout and purchase
    """
    # Core relationship
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        help_text="Owner of this shopping cart"
    )
    
    # Timestamp tracking
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When cart was first created for this user"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last time items were added/removed from cart"
    )

class CartItem(models.Model):
    """
    Individual items within a shopping cart
    Links specific products to quantities in user's cart
    """
    # Relationship fields
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='items',
        help_text="The shopping cart this item belongs to"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        help_text="The artwork/product being added to cart"
    )
    
    # Item details
    quantity = models.PositiveIntegerField(
        default=1,
        help_text="Number of this item in cart (usually 1 for unique artworks)"
    )
    
    # Metadata
    added_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this item was added to the cart"
    )

class Order(models.Model):
    """
    Completed purchase transactions
    Records all order details and tracks fulfillment status
    """
    # Order status progression
    STATUS_CHOICES = [
        ('pending', 'Pending'),       # Payment processing
        ('confirmed', 'Confirmed'),   # Payment successful, preparing shipment
        ('shipped', 'Shipped'),       # Package sent to customer
        ('delivered', 'Delivered'),   # Package received by customer
        ('cancelled', 'Cancelled'),   # Order cancelled before shipment
    ]
    
    # Core relationships and identification
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='orders',
        help_text="Customer who placed this order"
    )
    order_number = models.CharField(
        max_length=50, 
        unique=True,
        help_text="Unique identifier for tracking and customer service"
    )
    
    # Financial information
    total_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Total order value including taxes and shipping"
    )
    
    # Order status and fulfillment
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        help_text="Current order status for tracking progress"
    )
    
    # Shipping and delivery
    shipping_address = models.JSONField(
        help_text="Customer's delivery address stored as structured data"
    )
    
    # Payment information
    payment_method = models.CharField(
        max_length=50,
        help_text="How customer paid (credit card, PayPal, etc.)"
    )
    payment_status = models.CharField(
        max_length=20, 
        default='pending',
        help_text="Payment processing status (pending, completed, failed)"
    )
    
    # Timestamp tracking
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When order was placed by customer"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last time order status or details were updated"
    )
    
    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']

class OrderItem(models.Model):
    """
    Individual items within a completed order
    Preserves product details and pricing at time of purchase
    """
    # Relationship fields
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='items',
        help_text="The order this item belongs to"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        help_text="The artwork/product that was purchased"
    )
    
    # Purchase details
    quantity = models.PositiveIntegerField(
        default=1,
        help_text="Number of this item purchased (usually 1 for unique artworks)"
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Price paid for this item at time of purchase (preserves historical pricing)"
    )

class Wishlist(models.Model):
    """
    User's wishlist for saving favorite products
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'wishlists'
        unique_together = ['user', 'product']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.title}"

class ProductReview(models.Model):
    """
    User reviews and ratings for products
    """
    RATING_CHOICES = [(i, i) for i in range(1, 6)]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_reviews')
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'product_reviews'
        unique_together = ['product', 'reviewer']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.reviewer.username} - {self.product.title} ({self.rating}/5)"
