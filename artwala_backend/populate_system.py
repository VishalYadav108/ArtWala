#!/usr/bin/env python
"""
Comprehensive data population script for ArtWala
Creates 10 users, 5 artists, and populates the entire system with realistic data
"""

import os
import sys
import django
import random
from faker import Faker
from decimal import Decimal

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artwala_backend.settings')
django.setup()

from users.models import User
from artists.models import ArtistProfile, ArtistAnalytics, ArtistFollowing
from products.models import Category, Product, ProductReview, Wishlist, Cart, CartItem, Order, OrderItem
from chapters.models import Chapter, ChapterMembership, ChapterEvent, EventRegistration
from community.models import Forum, ForumPost, ForumComment, PostLike, CommentLike, JobPosting
from commissions.models import CommissionRequest, CommissionProposal, Message

fake = Faker()

def clear_existing_data():
    """Clear existing test data"""
    print("Clearing existing data...")
    
    # Clear in reverse dependency order
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    CartItem.objects.all().delete()
    Cart.objects.all().delete()
    ProductReview.objects.all().delete()
    Wishlist.objects.all().delete()
    Product.objects.all().delete()
    Category.objects.all().delete()
    
    EventRegistration.objects.all().delete()
    ChapterEvent.objects.all().delete()
    ChapterMembership.objects.all().delete()
    Chapter.objects.all().delete()
    
    CommentLike.objects.all().delete()
    PostLike.objects.all().delete()
    ForumComment.objects.all().delete()
    ForumPost.objects.all().delete()
    Forum.objects.all().delete()
    JobPosting.objects.all().delete()
    
    Message.objects.all().delete()
    CommissionProposal.objects.all().delete()
    CommissionRequest.objects.all().delete()
    
    ArtistFollowing.objects.all().delete()
    ArtistAnalytics.objects.all().delete()
    ArtistProfile.objects.all().delete()
    
    # Keep admin user, delete test users
    User.objects.filter(username__in=['john_artist', 'jane_artist']).delete()
    
    print("Existing data cleared!")

def create_users():
    """Create 10 diverse users"""
    print("Creating 10 users...")
    users = []
    
    user_data = [
        {'username': 'priya_artist', 'first_name': 'Priya', 'last_name': 'Sharma', 'user_type': 'artist'},
        {'username': 'rajesh_creator', 'first_name': 'Rajesh', 'last_name': 'Kumar', 'user_type': 'artist'},
        {'username': 'meera_painter', 'first_name': 'Meera', 'last_name': 'Patel', 'user_type': 'artist'},
        {'username': 'arjun_sculptor', 'first_name': 'Arjun', 'last_name': 'Singh', 'user_type': 'artist'},
        {'username': 'kavya_digital', 'first_name': 'Kavya', 'last_name': 'Nair', 'user_type': 'artist'},
        {'username': 'amit_collector', 'first_name': 'Amit', 'last_name': 'Gupta', 'user_type': 'buyer'},
        {'username': 'neha_enthusiast', 'first_name': 'Neha', 'last_name': 'Joshi', 'user_type': 'buyer'},
        {'username': 'vikram_buyer', 'first_name': 'Vikram', 'last_name': 'Rao', 'user_type': 'buyer'},
        {'username': 'shreya_fan', 'first_name': 'Shreya', 'last_name': 'Mishra', 'user_type': 'buyer'},
        {'username': 'rohit_patron', 'first_name': 'Rohit', 'last_name': 'Agarwal', 'user_type': 'buyer'},
    ]
    
    for i, data in enumerate(user_data):
        user = User.objects.create_user(
            username=data['username'],
            email=f"{data['username']}@artwala.com",
            password='testpass123',
            first_name=data['first_name'],
            last_name=data['last_name'],
            user_type=data['user_type'],
            bio=fake.text(max_nb_chars=200),
            location=fake.city() + ', India',
            phone=f"+91{fake.random_number(digits=10)}",
            is_verified=True
        )
        users.append(user)
        print(f"Created user: {user.username} ({user.user_type})")
    
    return users

def create_artists(users):
    """Create artist profiles for the first 5 users"""
    print("Creating 5 artist profiles...")
    artists = []
    
    artist_specializations = [
        ['Oil Painting', 'Landscape', 'Portraits'],
        ['Digital Art', 'Concept Art', 'Illustration'],
        ['Watercolor', 'Abstract Art', 'Modern Art'],
        ['Sculpture', 'Clay Work', '3D Art'],
        ['Photography', 'Digital Design', 'Mixed Media']
    ]
    
    artist_statements = [
        "I capture the beauty of nature through vibrant oil paintings that tell stories of our landscapes.",
        "Bringing imagination to life through digital art and concept designs for games and films.",
        "My watercolor abstracts explore emotions and human experiences through fluid forms and colors.",
        "I create sculptures that challenge perspectives and invite viewers to see the world differently.",
        "Through photography and digital design, I document life's fleeting moments and transform them into art."
    ]
    
    for i in range(5):
        user = users[i]  # First 5 users are artists
        artist = ArtistProfile.objects.create(
            user=user,
            display_name=f"{user.first_name} {user.last_name} Art Studio",
            slug=f"{user.username.replace('_', '-')}-studio",
            tagline=fake.catch_phrase(),
            artist_statement=artist_statements[i],
            specializations=artist_specializations[i],
            experience_years=random.randint(2, 15),
            rating=round(random.uniform(4.0, 5.0), 1),
            commission_available=True,
            commission_price_range=f"{random.randint(500, 2000)}-{random.randint(3000, 10000)}",
            response_time='1-3 days',
            featured=random.choice([True, False])
        )
        
        # Create analytics for each artist
        ArtistAnalytics.objects.create(
            artist=artist,
            total_sales=Decimal(random.randint(10000, 100000)),
            total_orders=random.randint(20, 150),
            total_commissions=random.randint(5, 30),
            profile_views=random.randint(500, 5000),
            products_sold=random.randint(15, 80),
            average_rating=Decimal(round(random.uniform(4.0, 5.0), 2))
        )
        
        artists.append(artist)
        print(f"Created artist: {artist.display_name}")
    
    return artists

def create_categories():
    """Create product categories"""
    print("Creating product categories...")
    categories = []
    
    category_data = [
        ('Paintings', 'paintings', 'Original paintings in various mediums'),
        ('Digital Art', 'digital-art', 'Digital artwork and illustrations'),
        ('Sculptures', 'sculptures', '3D artworks and sculptural pieces'),
        ('Photography', 'photography', 'Photographic art and prints'),
        ('Mixed Media', 'mixed-media', 'Artwork combining multiple mediums'),
        ('Drawings', 'drawings', 'Sketches, drawings, and line art'),
        ('Prints', 'prints', 'Limited edition prints and reproductions')
    ]
    
    for name, slug, desc in category_data:
        category = Category.objects.create(
            name=name,
            slug=slug,
            description=desc,
            is_active=True
        )
        categories.append(category)
        print(f"Created category: {name}")
    
    return categories

def create_products(artists, categories):
    """Create products for each artist"""
    print("Creating products...")
    products = []
    
    mediums = ['Oil on Canvas', 'Acrylic on Canvas', 'Watercolor on Paper', 'Digital Art', 
               'Charcoal on Paper', 'Mixed Media', 'Photography Print', 'Bronze Sculpture']
    
    dimensions = ['12x16 inches', '16x20 inches', '18x24 inches', '24x36 inches', 
                  '30x40 inches', '8x10 inches', '11x14 inches']
    
    art_titles = [
        'Sunset Over Mumbai', 'Morning Mist', 'Urban Dreams', 'Silent Waters', 
        'Dancing Colors', 'City Lights', 'Peaceful Valley', 'Abstract Thoughts',
        'Portrait of Hope', 'Monsoon Magic', 'Temple Bells', 'Market Street',
        'Ocean Waves', 'Mountain Peak', 'Garden Flowers', 'Night Sky',
        'Village Life', 'Modern Architecture', 'Traditional Dance', 'Spice Market'
    ]
    
    for artist in artists:
        # Each artist gets 4-6 products
        num_products = random.randint(4, 6)
        for i in range(num_products):
            title = random.choice(art_titles)
            product = Product.objects.create(
                title=f"{title} #{random.randint(1, 999)}",
                slug=f"{title.lower().replace(' ', '-')}-{random.randint(1, 999)}-{artist.slug}",
                artist=artist,
                category=random.choice(categories),
                description=fake.text(max_nb_chars=300),
                price=Decimal(random.randint(500, 15000)),
                medium=random.choice(mediums),
                dimensions=random.choice(dimensions),
                year_created=random.randint(2020, 2024),
                is_original=random.choice([True, False]),
                is_framed=random.choice([True, False]),
                weight=round(random.uniform(0.5, 5.0), 1),
                status='available',
                views_count=random.randint(10, 500),
                likes_count=random.randint(0, 50),
                featured=random.choice([True, False]),
                tags=['handmade', 'original', random.choice(['modern', 'traditional', 'contemporary'])]
            )
            products.append(product)
    
    print(f"Created {len(products)} products")
    return products

def create_chapters():
    """Create regional chapters"""
    print("Creating chapters...")
    chapters = []
    
    chapter_data = [
        ('Mumbai Chapter', 'mumbai-chapter', 'Mumbai', 'Maharashtra'),
        ('Delhi Chapter', 'delhi-chapter', 'Delhi', 'Delhi'),
        ('Bangalore Chapter', 'bangalore-chapter', 'Bangalore', 'Karnataka'),
        ('Chennai Chapter', 'chennai-chapter', 'Chennai', 'Tamil Nadu'),
        ('Pune Chapter', 'pune-chapter', 'Pune', 'Maharashtra'),
    ]
    
    admin_users = User.objects.filter(user_type='artist')[:5]
    
    for i, (name, slug, city, state) in enumerate(chapter_data):
        chapter = Chapter.objects.create(
            name=name,
            slug=slug,
            city=city,
            state=state,
            country='India',
            description=f"The vibrant art community of {city}, connecting local artists and art enthusiasts.",
            admin=admin_users[i],
            is_active=True,
            contact_email=f"{slug}@artwala.com"
        )
        chapters.append(chapter)
        print(f"Created chapter: {name}")
    
    return chapters

def create_forums():
    """Create community forums"""
    print("Creating forums...")
    forums = []
    
    forum_data = [
        ('General Discussion', 'general-discussion', 'General art discussions and community chat'),
        ('Technique Exchange', 'technique-exchange', 'Share and learn different art techniques'),
        ('Business & Career', 'business-career', 'Discussions about art business and career development'),
        ('Artist Showcase', 'artist-showcase', 'Show off your latest artworks and get feedback'),
        ('Beginner\'s Corner', 'beginners-corner', 'A welcoming space for new artists to learn'),
        ('Regional Meetups', 'regional-meetups', 'Organize and discuss local art events')
    ]
    
    for name, slug, desc in forum_data:
        forum = Forum.objects.create(
            name=name,
            slug=slug,
            description=desc,
            is_private=False
        )
        forums.append(forum)
        print(f"Created forum: {name}")
    
    return forums

def create_forum_content(forums, users):
    """Create forum posts and comments"""
    print("Creating forum posts and comments...")
    
    post_titles = [
        "Tips for pricing your artwork",
        "Best brushes for oil painting",
        "How to photograph your art",
        "Dealing with creative block",
        "Setting up your first studio",
        "Digital vs traditional art",
        "Building an online presence",
        "Color theory fundamentals",
        "Art exhibition opportunities",
        "Sustainable art practices"
    ]
    
    posts = []
    for i in range(15):  # Create 15 posts
        post = ForumPost.objects.create(
            forum=random.choice(forums),
            author=random.choice(users),
            title=random.choice(post_titles) + f" #{i+1}",
            slug=f"post-{i+1}-{fake.slug()}",
            content=fake.text(max_nb_chars=500),
            post_type=random.choice(['discussion', 'help', 'showcase']),
            tags=[fake.word(), fake.word()],
            views_count=random.randint(10, 200),
            likes_count=random.randint(0, 20)
        )
        posts.append(post)
        
        # Add comments to some posts
        if random.choice([True, False]):
            for j in range(random.randint(1, 4)):
                ForumComment.objects.create(
                    post=post,
                    author=random.choice(users),
                    content=fake.text(max_nb_chars=200),
                    likes_count=random.randint(0, 10)
                )
    
    print(f"Created {len(posts)} forum posts with comments")

def create_commissions(users, artists):
    """Create commission requests"""
    print("Creating commission requests...")
    
    commission_titles = [
        "Custom family portrait",
        "Company logo design",
        "Wedding painting",
        "Pet portrait commission",
        "Abstract wall art",
        "Digital character design",
        "Landscape painting",
        "Portrait sculpture"
    ]
    
    buyers = [u for u in users if u.user_type == 'buyer']
    
    for i in range(10):  # Create 10 commission requests
        CommissionRequest.objects.create(
            client=random.choice(buyers),
            artist=random.choice(artists),
            title=random.choice(commission_titles),
            description=fake.text(max_nb_chars=400),
            commission_type=random.choice(['painting', 'digital_art', 'portrait', 'sculpture']),
            budget_min=Decimal(random.randint(1000, 3000)),
            budget_max=Decimal(random.randint(3000, 10000)),
            deadline=fake.date_between(start_date='+1m', end_date='+6m'),
            status=random.choice(['submitted', 'under_review', 'accepted', 'in_progress']),
            dimensions="24x36 inches",
            additional_requirements=fake.text(max_nb_chars=200)
        )
    
    print("Created 10 commission requests")

def create_reviews_and_engagement(products, users):
    """Create product reviews, wishlists, and user engagement"""
    print("Creating reviews and user engagement...")
    
    # Create product reviews
    buyers = [u for u in users if u.user_type == 'buyer']
    for product in random.sample(products, min(15, len(products))):
        reviewer = random.choice(buyers)
        ProductReview.objects.create(
            product=product,
            reviewer=reviewer,
            rating=random.randint(4, 5),
            comment=fake.text(max_nb_chars=150)
        )
    
    # Create wishlists
    for buyer in buyers:
        wishlist_products = random.sample(products, random.randint(2, 6))
        for product in wishlist_products:
            Wishlist.objects.create(user=buyer, product=product)
    
    # Create artist followings
    for buyer in buyers:
        followed_artists = random.sample(list(ArtistProfile.objects.all()), random.randint(1, 3))
        for artist in followed_artists:
            ArtistFollowing.objects.create(follower=buyer, artist=artist)
    
    print("Created reviews, wishlists, and followings")

def populate_system():
    """Main function to populate the entire system"""
    print("🎨 Starting comprehensive ArtWala system population...")
    print("=" * 60)
    
    # Clear existing data
    clear_existing_data()
    
    # Create users and artists
    users = create_users()
    artists = create_artists(users)
    
    # Create product system
    categories = create_categories()
    products = create_products(artists, categories)
    
    # Create community system
    chapters = create_chapters()
    forums = create_forums()
    create_forum_content(forums, users)
    
    # Create commerce system
    create_commissions(users, artists)
    create_reviews_and_engagement(products, users)
    
    print("=" * 60)
    print("🎉 System population completed successfully!")
    print(f"Created:")
    print(f"  • {len(users)} users (5 artists, 5 buyers)")
    print(f"  • {len(artists)} artist profiles with analytics")
    print(f"  • {len(categories)} product categories")
    print(f"  • {len(products)} products")
    print(f"  • {len(chapters)} regional chapters")
    print(f"  • {len(forums)} community forums")
    print(f"  • Forum posts, comments, and engagement")
    print(f"  • Commission requests and proposals")
    print(f"  • Product reviews, wishlists, and followings")
    print()
    print("🚀 Your ArtWala system is now fully populated with realistic data!")

if __name__ == '__main__':
    populate_system()
