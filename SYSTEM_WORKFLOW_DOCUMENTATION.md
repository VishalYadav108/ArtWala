# ARTWALA System Architecture & Workflow Documentation

## System Overview

ARTWALA is a comprehensive full-stack art marketplace platform designed to connect artists with art enthusiasts across India. The system facilitates artwork discovery, purchasing, community building, and custom commission workflows through a modern web application built with Django backend and React frontend.

## Detailed System Architecture

### 1. Backend Architecture (Django)

#### 1.1 Core Framework
- **Django 5.2.4**: Main web framework providing ORM, admin interface, and security
- **Django REST Framework**: Handles API serialization, authentication, and viewsets
- **SQLite/PostgreSQL**: Database layer for development and production respectively
- **CORS Headers**: Enables cross-origin requests from React frontend

#### 1.2 Modular App Structure

**Users App (`users/`)**
- Custom User model extending Django's AbstractUser
- Additional fields: phone_number, date_of_birth, address, profile_picture
- Token-based authentication system
- User registration, login, and profile management APIs

**Artists App (`artists/`)**
- ArtistProfile model linked to User via OneToOne relationship
- Fields: bio, specialty, years_of_experience, portfolio_website, social_links
- Artist verification system with is_verified boolean field
- Rating system with average_rating calculation
- Artist review and testimonial management

**Products App (`products/`)**
- Product model representing individual artworks
- Category model for artwork classification (Paintings, Sculptures, Digital Art, etc.)
- ProductImage model for multiple artwork images
- Shopping cart functionality with Cart and CartItem models
- Order management with Order and OrderItem models
- Product likes/wishlist system
- Inventory management with stock quantities

**Chapters App (`chapters/`)**
- Chapter model representing city-based artist communities
- ChapterMembership for artist-chapter relationships
- ChapterEvent model for organizing local events
- EventRegistration for event attendance tracking
- Chapter admin roles and permissions

**Community App (`community/`)**
- Forum model for different discussion categories
- ForumPost model for user-generated content
- Post categorization (discussion, job, collaboration, help, showcase)
- Comment system with ForumComment model
- Like system for posts and comments
- Job posting functionality for freelance opportunities

**Commissions App (`commissions/`)**
- CommissionRequest model for custom artwork orders
- CommissionProposal model for artist responses
- CommissionContract for agreed terms and conditions
- CommissionMilestone for project progress tracking
- Payment integration ready with CommissionPayment model
- Review system for completed commissions

#### 1.3 Database Relationships

```
User (1) ←→ (1) ArtistProfile
User (1) ←→ (N) Product (via ArtistProfile)
User (1) ←→ (N) Cart
Cart (1) ←→ (N) CartItem
User (1) ←→ (N) Order
Order (1) ←→ (N) OrderItem
Chapter (1) ←→ (N) ChapterMembership ←→ (1) ArtistProfile
Chapter (1) ←→ (N) ChapterEvent
User (1) ←→ (N) ForumPost
User (1) ←→ (N) CommissionRequest
ArtistProfile (1) ←→ (N) CommissionProposal
```

#### 1.4 API Design

**RESTful Endpoints:**
- GET, POST, PUT, DELETE operations for all resources
- Pagination with PageNumberPagination (20 items per page)
- Filtering and search capabilities
- Proper HTTP status codes and error handling
- Token-based authentication for protected endpoints

### 2. Frontend Architecture (React)

#### 2.1 Component Structure
- **App.js**: Main application component with routing
- **Dashboard.js**: Central dashboard displaying overview data
- **Authentication Components**: Login, register, profile management
- **Product Components**: Product listing, details, search, cart
- **Artist Components**: Artist profiles, portfolios, reviews
- **Community Components**: Forums, posts, discussions
- **Commission Components**: Request forms, proposal management

#### 2.2 State Management
- React Hooks (useState, useEffect) for local component state
- Context API for global state (user authentication, cart)
- Local storage for persisting user sessions

#### 2.3 API Integration
- Axios HTTP client for backend communication
- Interceptors for authentication headers
- Error handling with user-friendly messages
- Loading states and retry mechanisms

## System Workflow Details

### 3. User Journey Workflows

#### 3.1 New User Registration & Artist Onboarding

**Step 1: User Registration**
1. User visits ARTWALA website
2. Clicks "Sign Up" and fills registration form
3. Frontend sends POST request to `/api/auth/register/`
4. Django creates User instance with basic details
5. Email verification sent (future enhancement)
6. User redirected to profile completion

**Step 2: Artist Profile Creation**
1. User selects "I'm an Artist" option
2. Fills artist-specific information form
3. Frontend sends POST request to `/api/artists/profiles/`
4. Django creates ArtistProfile linked to User
5. Artist can upload portfolio images
6. Profile pending verification by admin

**Step 3: Chapter Membership**
1. Artist browses available city chapters
2. Selects local chapter and requests membership
3. Chapter admin approves/rejects membership
4. Artist gains access to chapter events and local community

#### 3.2 Product Listing & Sales Workflow

**Step 1: Product Creation**
1. Verified artist accesses "Add Product" form
2. Fills artwork details (title, description, price, category)
3. Uploads multiple product images
4. Sets inventory quantity and shipping details
5. Frontend sends POST request to `/api/products/products/`
6. Django creates Product instance with "draft" status

**Step 2: Product Publishing**
1. Artist reviews product details
2. Changes status from "draft" to "published"
3. Product becomes visible in marketplace
4. Automatic notifications to followers (future enhancement)

**Step 3: Product Discovery & Purchase**
1. Buyers browse products by category/search
2. View product details and artist profiles
3. Add items to cart via POST to `/api/products/cart/`
4. Proceed to checkout and payment
5. Order created with "pending" status
6. Payment processing triggers order confirmation

#### 3.3 Commission Workflow

**Step 1: Commission Request**
1. Buyer browses artist profiles
2. Clicks "Request Commission" on artist page
3. Fills commission details form (description, budget, timeline)
4. Frontend sends POST request to `/api/commissions/requests/`
5. Django creates CommissionRequest with "pending" status

**Step 2: Artist Response**
1. Artist receives notification of commission request
2. Reviews request details and client requirements
3. Creates proposal with pricing and timeline
4. Sends POST request to `/api/commissions/proposals/`
5. Client receives notification of proposal

**Step 3: Contract & Execution**
1. Client reviews and accepts/rejects proposal
2. Upon acceptance, CommissionContract created
3. Milestone-based payment system activated
4. Artist updates progress via milestone completion
5. Final delivery and review completion

#### 3.4 Community Engagement Workflow

**Step 1: Forum Participation**
1. Users browse available forums
2. Create new posts or reply to existing ones
3. Post categorization (discussion, job, help, showcase)
4. Like and comment on community content

**Step 2: Chapter Events**
1. Chapter admins create local events
2. Members receive event notifications
3. Event registration and attendance tracking
4. Post-event feedback and networking

### 4. Business Logic Implementation

#### 4.1 Authentication & Authorization

**User Authentication:**
```python
# Token-based authentication
user = authenticate(username=username, password=password)
if user:
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})
```

**Permission Classes:**
- `IsAuthenticated`: For user-specific data
- `IsAuthenticatedOrReadOnly`: For public browsing with authenticated actions
- `IsOwnerOrReadOnly`: For user's own content management

#### 4.2 Search & Filtering

**Product Search:**
- Text search across title, description, tags
- Category-based filtering
- Price range filtering
- Artist-based filtering
- Sort by: price, date, popularity, rating

**Artist Search:**
- Specialty-based filtering
- Location-based search
- Experience level filtering
- Rating and review-based sorting

#### 4.3 Recommendation System (Future Enhancement)

**Product Recommendations:**
- User browsing history analysis
- Purchase pattern matching
- Artist style similarity
- Category preference learning

**Artist Recommendations:**
- Commission history compatibility
- Style and medium matching
- Price range compatibility
- Review and rating analysis

### 5. Data Flow Architecture

#### 5.1 Request-Response Cycle

```
Frontend (React) → API Request → Django URL Router → View Function → 
Model Interaction → Database Query → Serializer → JSON Response → 
Frontend State Update → UI Re-render
```

#### 5.2 Real-time Features (Future Enhancement)

**WebSocket Integration:**
- Real-time notifications for new messages
- Live commission status updates
- Event announcements
- Chat system for buyer-artist communication

### 6. Security Implementation

#### 6.1 Authentication Security
- Token expiration and refresh mechanisms
- Password hashing with Django's built-in PBKDF2
- Rate limiting for API endpoints
- CSRF protection for form submissions

#### 6.2 Data Validation
- Frontend form validation with real-time feedback
- Backend serializer validation for data integrity
- File upload validation for images
- SQL injection prevention via ORM

#### 6.3 Authorization Levels
- Public: Browse products and artists
- Authenticated: Create account, purchase, basic community access
- Artist: Create products, manage portfolio, accept commissions
- Chapter Admin: Manage local chapter and events
- Super Admin: Platform-wide management and verification

### 7. Performance Optimization

#### 7.1 Database Optimization
- Database indexing on frequently queried fields
- Query optimization with select_related and prefetch_related
- Pagination for large datasets
- Database connection pooling

#### 7.2 Frontend Optimization
- Component-level code splitting
- Image lazy loading and optimization
- API response caching
- Debounced search inputs

#### 7.3 Scalability Considerations
- Microservices architecture for future scaling
- CDN integration for static files
- Load balancing for high traffic
- Database sharding for large datasets

### 8. Integration Points

#### 8.1 Payment Gateway Integration
- Razorpay for Indian market
- Stripe for international transactions
- Wallet integration (Paytm, PhonePe)
- Cryptocurrency payment support (future)

#### 8.2 Third-party Services
- AWS S3 for file storage
- SendGrid for email notifications
- Google Maps for location services
- Social media login integration

#### 8.3 Mobile Application
- React Native for cross-platform mobile app
- Shared API endpoints with web application
- Push notifications for mobile users
- Offline browsing capabilities

### 9. Analytics & Monitoring

#### 9.1 User Analytics
- User journey tracking
- Conversion rate optimization
- Artist performance metrics
- Revenue analytics and reporting

#### 9.2 System Monitoring
- API response time monitoring
- Database performance tracking
- Error logging and alerting
- User feedback collection

### 10. Future Enhancements

#### 10.1 AI/ML Features
- Image recognition for artwork categorization
- Style similarity analysis
- Fraud detection for transactions
- Personalized recommendation engine

#### 10.2 Advanced Features
- Virtual gallery tours
- Augmented reality for wall placement
- Live streaming for artist demonstrations
- Blockchain for artwork authentication

#### 10.3 Marketplace Expansion
- International shipping integration
- Multi-language support
- Currency conversion
- Regional chapter expansion

## Conclusion

ARTWALA represents a comprehensive digital ecosystem for the art community, combining e-commerce functionality with social networking and professional services. The modular architecture ensures scalability and maintainability while providing a rich user experience for all stakeholders in the art marketplace.

The system's design emphasizes user experience, data integrity, and business logic that supports the unique needs of artists and art enthusiasts. With proper implementation of the outlined workflows and future enhancements, ARTWALA can become a leading platform in the digital art marketplace space.
