from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from artists.models import ArtistProfile, ArtistReview
from products.models import Category, Product, ProductImage, Cart, CartItem, Order, OrderItem
from chapters.models import Chapter, ChapterMembership, ChapterEvent
from community.models import Forum, ForumPost, JobPosting
from commissions.models import CommissionRequest, CommissionProposal
from decimal import Decimal
import random
from datetime import date, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create Users
        self.create_users()
        
        # Create Categories
        self.create_categories()
        
        # Create Artist Profiles
        self.create_artist_profiles()
        
        # Create Products
        self.create_products()
        
        # Create Chapters
        self.create_chapters()
        
        # Create Community Data
        self.create_community_data()
        
        # Create Commission Requests
        self.create_commission_requests()
        
        # Create Sample Orders
        self.create_orders()
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data!'))
    
    def create_users(self):
        self.stdout.write('Creating users...')
        
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            email='admin@artwala.org',
            defaults={
                'username': 'admin',
                'first_name': 'Admin',
                'last_name': 'User',
                'user_type': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'is_verified': True,
                'bio': 'ARTWALA Platform Administrator',
                'location': 'Mumbai, India'
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
        
        # Create sample artists
        artists_data = [
            {
                'email': 'priya.sharma@gmail.com',
                'username': 'priya_art',
                'first_name': 'Priya',
                'last_name': 'Sharma',
                'user_type': 'artist',
                'location': 'Delhi, India',
                'bio': 'Contemporary artist specializing in oil paintings and mixed media.',
                'website': 'https://priyasharmaart.com'
            },
            {
                'email': 'rajesh.patel@gmail.com',
                'username': 'rajesh_sculptor',
                'first_name': 'Rajesh',
                'last_name': 'Patel',
                'user_type': 'artist',
                'location': 'Ahmedabad, Gujarat',
                'bio': 'Bronze sculptor with 15 years of experience in traditional and modern art.',
                'website': 'https://rajeshpatelart.com'
            },
            {
                'email': 'anita.roy@gmail.com',
                'username': 'anita_watercolors',
                'first_name': 'Anita',
                'last_name': 'Roy',
                'user_type': 'artist',
                'location': 'Kolkata, West Bengal',
                'bio': 'Watercolor artist inspired by nature and urban landscapes.',
                'website': 'https://anitaroyart.com'
            },
            {
                'email': 'vikram.singh@gmail.com',
                'username': 'vikram_digital',
                'first_name': 'Vikram',
                'last_name': 'Singh',
                'user_type': 'artist',
                'location': 'Bangalore, Karnataka',
                'bio': 'Digital artist and illustrator specializing in concept art and character design.',
                'website': 'https://vikramsingh.design'
            }
        ]
        
        for artist_data in artists_data:
            user, created = User.objects.get_or_create(
                email=artist_data['email'],
                defaults={**artist_data, 'is_verified': True}
            )
            if created:
                user.set_password('artist123')
                user.save()
        
        # Create sample buyers
        buyers_data = [
            {
                'email': 'buyer1@gmail.com',
                'username': 'art_lover_1',
                'first_name': 'Amit',
                'last_name': 'Kumar',
                'user_type': 'buyer',
                'location': 'Mumbai, Maharashtra',
                'bio': 'Art collector and enthusiast'
            },
            {
                'email': 'buyer2@gmail.com',
                'username': 'collector_sara',
                'first_name': 'Sara',
                'last_name': 'Gupta',
                'user_type': 'buyer',
                'location': 'Pune, Maharashtra',
                'bio': 'Interior designer who loves contemporary art'
            }
        ]
        
        for buyer_data in buyers_data:
            user, created = User.objects.get_or_create(
                email=buyer_data['email'],
                defaults={**buyer_data, 'is_verified': True}
            )
            if created:
                user.set_password('buyer123')
                user.save()
    
    def create_categories(self):
        self.stdout.write('Creating categories...')
        
        categories = [
            {'name': 'Paintings', 'slug': 'paintings', 'description': 'Oil, acrylic, watercolor paintings'},
            {'name': 'Sculptures', 'slug': 'sculptures', 'description': 'Bronze, marble, wood sculptures'},
            {'name': 'Digital Art', 'slug': 'digital-art', 'description': 'Digital illustrations and concept art'},
            {'name': 'Photography', 'slug': 'photography', 'description': 'Fine art photography'},
            {'name': 'Mixed Media', 'slug': 'mixed-media', 'description': 'Mixed media artworks'},
            {'name': 'Drawings', 'slug': 'drawings', 'description': 'Pencil, charcoal, ink drawings'}
        ]
        
        for cat_data in categories:
            Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
    
    def create_artist_profiles(self):
        self.stdout.write('Creating artist profiles...')
        
        artists = User.objects.filter(user_type='artist')
        profiles_data = [
            {
                'display_name': 'Priya Sharma Arts',
                'tagline': 'Contemporary Art with Traditional Soul',
                'specializations': ['oil_painting', 'mixed_media', 'contemporary_art'],
                'experience_years': 8,
                'commission_available': True,
                'commission_price_range': '₹15,000 - ₹1,50,000',
                'artist_statement': 'My work explores the intersection of traditional Indian motifs with contemporary expression.'
            },
            {
                'display_name': 'Rajesh Patel Sculptures',
                'tagline': 'Bringing Stories to Life in Bronze',
                'specializations': ['sculpture', 'bronze_casting', 'public_art'],
                'experience_years': 15,
                'commission_available': True,
                'commission_price_range': '₹50,000 - ₹5,00,000',
                'artist_statement': 'Each sculpture tells a story that connects the viewer with human emotions and experiences.'
            },
            {
                'display_name': 'Anita Roy Watercolors',
                'tagline': 'Capturing Moments in Fluid Beauty',
                'specializations': ['watercolor', 'landscape', 'urban_sketching'],
                'experience_years': 12,
                'commission_available': True,
                'commission_price_range': '₹5,000 - ₹75,000',
                'artist_statement': 'Watercolors allow me to capture the ephemeral beauty of light and atmosphere.'
            },
            {
                'display_name': 'Vikram Singh Digital',
                'tagline': 'Imagination Meets Technology',
                'specializations': ['digital_art', 'concept_art', 'character_design'],
                'experience_years': 6,
                'commission_available': True,
                'commission_price_range': '₹10,000 - ₹1,00,000',
                'artist_statement': 'Digital art opens infinite possibilities for creative expression and storytelling.'
            }
        ]
        
        for i, artist in enumerate(artists):
            if i < len(profiles_data):
                profile_data = profiles_data[i]
                ArtistProfile.objects.get_or_create(
                    user=artist,
                    defaults={
                        **profile_data,
                        'rating': Decimal(str(round(random.uniform(4.0, 5.0), 1))),
                        'total_reviews': random.randint(5, 25),
                        'featured': i < 2  # First 2 artists are featured
                    }
                )
    
    def create_products(self):
        self.stdout.write('Creating products...')
        
        categories = list(Category.objects.all())
        artist_profiles = list(ArtistProfile.objects.all())
        
        products_data = [
            {
                'title': 'Sunset Over Ganges',
                'description': 'A beautiful oil painting capturing the serene sunset over the holy river Ganges.',
                'price': Decimal('25000.00'),
                'dimensions': '24x36 inches',
                'medium': 'Oil on canvas',
                'year_created': 2023,
                'is_original': True,
                'is_framed': True,
                'status': 'published',
                'tags': ['sunset', 'ganges', 'spiritual', 'landscape']
            },
            {
                'title': 'Dancing Shiva Bronze',
                'description': 'Traditional bronze sculpture of Nataraja, the cosmic dancer.',
                'price': Decimal('85000.00'),
                'dimensions': '18x12x8 inches',
                'medium': 'Bronze',
                'year_created': 2023,
                'weight': Decimal('5.5'),
                'is_original': True,
                'status': 'published',
                'tags': ['shiva', 'bronze', 'traditional', 'sculpture']
            },
            {
                'title': 'Monsoon Streets',
                'description': 'Watercolor painting of busy Indian streets during monsoon.',
                'price': Decimal('12000.00'),
                'dimensions': '16x20 inches',
                'medium': 'Watercolor on paper',
                'year_created': 2024,
                'is_original': True,
                'is_framed': True,
                'status': 'published',
                'tags': ['monsoon', 'street', 'urban', 'watercolor']
            },
            {
                'title': 'Cyber Warrior',
                'description': 'Digital concept art featuring a futuristic warrior character.',
                'price': Decimal('15000.00'),
                'dimensions': 'Digital - 4K Resolution',
                'medium': 'Digital Art',
                'year_created': 2024,
                'is_original': True,
                'status': 'published',
                'tags': ['cyberpunk', 'warrior', 'futuristic', 'character']
            },
            {
                'title': 'Abstract Emotions',
                'description': 'Mixed media artwork exploring human emotions through color and texture.',
                'price': Decimal('18000.00'),
                'dimensions': '20x24 inches',
                'medium': 'Mixed media on canvas',
                'year_created': 2023,
                'is_original': True,
                'status': 'published',
                'tags': ['abstract', 'emotions', 'contemporary', 'mixed_media']
            }
        ]
        
        for i, product_data in enumerate(products_data):
            artist = artist_profiles[i % len(artist_profiles)]
            category = categories[i % len(categories)]
            
            product, created = Product.objects.get_or_create(
                title=product_data['title'],
                artist=artist,
                defaults={
                    **product_data,
                    'category': category,
                    'slug': product_data['title'].lower().replace(' ', '-'),
                    'views_count': random.randint(50, 500),
                    'likes_count': random.randint(5, 50),
                    'featured': i < 3
                }
            )
    
    def create_chapters(self):
        self.stdout.write('Creating chapters...')
        
        admin_user = User.objects.filter(user_type='admin').first()
        
        chapters_data = [
            {
                'name': 'Mumbai Chapter',
                'slug': 'mumbai',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'description': 'ARTWALA Mumbai chapter promoting local artists and art culture.',
                'contact_email': 'mumbai@artwala.org',
                'contact_phone': '+91-98765-43210'
            },
            {
                'name': 'Delhi Chapter',
                'slug': 'delhi',
                'city': 'Delhi',
                'state': 'Delhi',
                'description': 'ARTWALA Delhi chapter connecting artists in the capital region.',
                'contact_email': 'delhi@artwala.org',
                'contact_phone': '+91-98765-43211'
            },
            {
                'name': 'Bangalore Chapter',
                'slug': 'bangalore',
                'city': 'Bangalore',
                'state': 'Karnataka',
                'description': 'ARTWALA Bangalore chapter fostering tech-art collaborations.',
                'contact_email': 'bangalore@artwala.org',
                'contact_phone': '+91-98765-43212'
            }
        ]
        
        for chapter_data in chapters_data:
            Chapter.objects.get_or_create(
                slug=chapter_data['slug'],
                defaults={**chapter_data, 'admin': admin_user}
            )
    
    def create_community_data(self):
        self.stdout.write('Creating community data...')
        
        # Create Forums
        forums_data = [
            {
                'name': 'General Discussion',
                'slug': 'general',
                'description': 'General discussions about art and creativity'
            },
            {
                'name': 'Technique Exchange',
                'slug': 'techniques',
                'description': 'Share and learn different art techniques'
            },
            {
                'name': 'Business & Career',
                'slug': 'business',
                'description': 'Discussions about art business and career development'
            }
        ]
        
        for forum_data in forums_data:
            Forum.objects.get_or_create(
                slug=forum_data['slug'],
                defaults=forum_data
            )
        
        # Create Job Postings
        artists = User.objects.filter(user_type='artist')
        buyers = User.objects.filter(user_type='buyer')
        
        if buyers.exists():
            JobPosting.objects.get_or_create(
                title='Mural Artist for Restaurant',
                defaults={
                    'posted_by': buyers.first(),
                    'slug': 'mural-artist-restaurant',
                    'description': 'Looking for an experienced mural artist to create artwork for our new restaurant.',
                    'company': 'Spice Garden Restaurant',
                    'location': 'Mumbai, Maharashtra',
                    'job_type': 'freelance',
                    'salary_range': '₹1,00,000 - ₹2,50,000',
                    'requirements': 'Experience in large-scale murals, portfolio required',
                    'contact_email': 'hr@spicegarden.com',
                    'application_deadline': date.today() + timedelta(days=30)
                }
            )
    
    def create_commission_requests(self):
        self.stdout.write('Creating commission requests...')
        
        buyers = User.objects.filter(user_type='buyer')
        artist_profiles = ArtistProfile.objects.all()
        
        if buyers.exists() and artist_profiles.exists():
            CommissionRequest.objects.get_or_create(
                title='Custom Family Portrait',
                defaults={
                    'client': buyers.first(),
                    'artist': artist_profiles.first(),
                    'description': 'Looking for a custom oil painting portrait of my family (4 members).',
                    'commission_type': 'portrait',
                    'budget_min': Decimal('40000.00'),
                    'budget_max': Decimal('60000.00'),
                    'deadline': date.today() + timedelta(days=45),
                    'dimensions': '24x30 inches',
                    'additional_requirements': 'Traditional style preferred, should include pets',
                    'status': 'submitted'
                }
            )
    
    def create_orders(self):
        self.stdout.write('Creating sample orders...')
        
        buyers = User.objects.filter(user_type='buyer')
        products = Product.objects.filter(status='published')
        
        if buyers.exists() and products.exists():
            buyer = buyers.first()
            product = products.first()
            
            # Create cart first
            cart, created = Cart.objects.get_or_create(user=buyer)
            
            # Create order
            order, created = Order.objects.get_or_create(
                order_number='ORD-2024-001',
                defaults={
                    'user': buyer,
                    'total_amount': product.price,
                    'status': 'confirmed',
                    'shipping_address': {
                        'name': f"{buyer.first_name} {buyer.last_name}",
                        'address': '123 Art Street',
                        'city': 'Mumbai',
                        'state': 'Maharashtra',
                        'pincode': '400001',
                        'phone': '+91-9876543210'
                    },
                    'payment_method': 'razorpay',
                    'payment_status': 'completed'
                }
            )
            
            if created:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=1,
                    price=product.price
                )
