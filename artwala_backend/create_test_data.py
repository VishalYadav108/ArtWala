#!/usr/bin/env python

# Create test data for ArtWala

import os
import sys
import django

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artwala_backend.settings')
django.setup()

from users.models import User
from artists.models import ArtistProfile
from products.models import Category, Product
from chapters.models import Chapter
from community.models import Forum

def create_test_data():
    print("Creating test data...")
    
    # Create test users
    try:
        user1 = User.objects.get_or_create(
            username='john_artist',
            defaults={
                'email': 'john@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'user_type': 'artist'
            }
        )[0]
        
        user2 = User.objects.get_or_create(
            username='jane_artist',
            defaults={
                'email': 'jane@example.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'user_type': 'artist'
            }
        )[0]
        
        print(f"Created users: {user1.username}, {user2.username}")
    except Exception as e:
        print(f"Error creating users: {e}")
    
    # Create artist profiles
    try:
        artist1 = ArtistProfile.objects.get_or_create(
            user=user1,
            defaults={
                'display_name': 'John Doe Art',
                'slug': 'john-doe-art',
                'tagline': 'Modern Abstract Artist',
                'artist_statement': 'I create vibrant abstract paintings that capture emotions.',
                'specializations': ['Painting', 'Abstract Art'],
                'experience_years': 5,
                'rating': 4.5,
                'commission_available': True,
                'commission_price_range': '500-2000'
            }
        )[0]
        
        artist2 = ArtistProfile.objects.get_or_create(
            user=user2,
            defaults={
                'display_name': 'Jane Smith Studio',
                'slug': 'jane-smith-studio',
                'tagline': 'Portrait and Figure Drawing Specialist',
                'artist_statement': 'Capturing the essence of people through realistic portraits.',
                'specializations': ['Drawing', 'Portraits'],
                'experience_years': 8,
                'rating': 4.8,
                'commission_available': True,
                'commission_price_range': '300-1500'
            }
        )[0]
        
        print(f"Created artist profiles: {artist1.display_name}, {artist2.display_name}")
    except Exception as e:
        print(f"Error creating artist profiles: {e}")
    
    # Create categories
    try:
        painting_cat = Category.objects.get_or_create(
            name='Paintings',
            defaults={
                'slug': 'paintings',
                'description': 'Original paintings in various mediums'
            }
        )[0]
        
        drawing_cat = Category.objects.get_or_create(
            name='Drawings',
            defaults={
                'slug': 'drawings',
                'description': 'Sketches, portraits, and figure drawings'
            }
        )[0]
        
        print(f"Created categories: {painting_cat.name}, {drawing_cat.name}")
    except Exception as e:
        print(f"Error creating categories: {e}")
    
    # Create products
    try:
        product1 = Product.objects.get_or_create(
            title='Sunset Dreams',
            defaults={
                'slug': 'sunset-dreams',
                'artist': artist1,
                'category': painting_cat,
                'description': 'A vibrant abstract painting capturing the essence of a sunset',
                'price': 750.00,
                'medium': 'Acrylic on Canvas',
                'dimensions': '24x36 inches',
                'year_created': 2024,
                'is_original': True,
                'status': 'available'
            }
        )[0]
        
        product2 = Product.objects.get_or_create(
            title='City Portrait',
            defaults={
                'slug': 'city-portrait',
                'artist': artist2,
                'category': drawing_cat,
                'description': 'Detailed charcoal portrait of urban life',
                'price': 450.00,
                'medium': 'Charcoal on Paper',
                'dimensions': '18x24 inches',
                'year_created': 2024,
                'is_original': True,
                'status': 'available'
            }
        )[0]
        
        product3 = Product.objects.get_or_create(
            title='Ocean Waves',
            defaults={
                'slug': 'ocean-waves',
                'artist': artist1,
                'category': painting_cat,
                'description': 'Abstract representation of ocean movements',
                'price': 900.00,
                'medium': 'Oil on Canvas',
                'dimensions': '30x40 inches',
                'year_created': 2024,
                'is_original': True,
                'status': 'available'
            }
        )[0]
        
        print(f"Created products: {product1.title}, {product2.title}, {product3.title}")
    except Exception as e:
        print(f"Error creating products: {e}")
    
    # Create chapters
    try:
        mumbai_chapter = Chapter.objects.get_or_create(
            name='Mumbai Chapter',
            defaults={
                'slug': 'mumbai-chapter',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'country': 'India',
                'description': 'The vibrant art community of Mumbai',
                'admin': user1,
                'contact_email': 'mumbai@artwala.com'
            }
        )[0]
        
        delhi_chapter = Chapter.objects.get_or_create(
            name='Delhi Chapter',
            defaults={
                'slug': 'delhi-chapter',
                'city': 'Delhi',
                'state': 'Delhi',
                'country': 'India',
                'description': 'Art enthusiasts and creators in the capital',
                'admin': user2,
                'contact_email': 'delhi@artwala.com'
            }
        )[0]
        
        print(f"Created chapters: {mumbai_chapter.name}, {delhi_chapter.name}")
    except Exception as e:
        print(f"Error creating chapters: {e}")
    
    # Create forums
    try:
        general_forum = Forum.objects.get_or_create(
            name='General Discussion',
            defaults={
                'slug': 'general-discussion',
                'description': 'General art-related discussions and community chat'
            }
        )[0]
        
        technique_forum = Forum.objects.get_or_create(
            name='Technique Tips',
            defaults={
                'slug': 'technique-tips',
                'description': 'Share and learn artistic techniques and methods'
            }
        )[0]
        
        showcase_forum = Forum.objects.get_or_create(
            name='Artist Showcase',
            defaults={
                'slug': 'artist-showcase',
                'description': 'Show off your latest artworks and get feedback'
            }
        )[0]
        
        print(f"Created forums: {general_forum.name}, {technique_forum.name}, {showcase_forum.name}")
    except Exception as e:
        print(f"Error creating forums: {e}")
    
    print("Test data creation completed!")

if __name__ == '__main__':
    create_test_data()
