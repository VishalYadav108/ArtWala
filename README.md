# ARTWALA - Full-Stack Art Marketplace Platform

[![Django](https://img.shields.io/badge/Django-5.2.4-092E20?style=flat&logo=django&logoColor=white)](https://djangoproject.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat&logo=react&logoColor=black)](https://reactjs.org/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?style=flat&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

> A comprehensive full-stack web application for an art marketplace, connecting artists with art enthusiasts across India.

## 🎨 Project Overview

ARTWALA is a modern art marketplace platform that enables artists to showcase and sell their artwork while providing art enthusiasts with a curated platform to discover and purchase unique pieces. The platform features city-based chapters, community forums, and a comprehensive commission system.

## 🏗️ Architecture

### Backend (Django)
- **Framework**: Django 5.2.4 with Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **API**: RESTful API with proper serialization and pagination
- **Authentication**: Token-based authentication system
- **CORS**: Configured for React frontend integration

### Frontend (React)
- **Framework**: React 18 with Create React App
- **HTTP Client**: Axios for API communication
- **State Management**: React hooks (useState/useEffect)
- **Styling**: Responsive design with inline styles

## 🚀 Features

### ✅ Implemented
- **User Management**: Custom user model with authentication
- **Artist Profiles**: Comprehensive artist portfolio management
- **Product Catalog**: Artwork listings with categories and search
- **Shopping System**: Cart and order management
- **City Chapters**: Location-based artist communities
- **Community Forums**: Discussion boards and job postings
- **Commission System**: Custom artwork request workflow
- **RESTful API**: Complete backend API with serializers
- **Frontend Integration**: React dashboard with API connectivity

### 🔮 Future Development
- Payment gateway integration (Razorpay/Stripe)
- Advanced search and filtering
- Real-time notifications
- File upload for artwork images
- Email notifications
- Admin dashboard
- Mobile app (React Native)

## 📁 Project Structure

```
ArtWala/
├── artwala_backend/          # Django Backend
│   ├── users/               # User management
│   ├── artists/             # Artist profiles
│   ├── products/            # Product catalog
│   ├── chapters/            # City chapters
│   ├── community/           # Forums & discussions
│   ├── commissions/         # Commission system
│   └── artwala_backend/     # Main settings
├── artwala-frontend/        # React Frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.js          # Main app
│   │   └── index.js        # Entry point
│   └── public/
├── PROJECT_SUMMARY.md       # Detailed documentation
└── README.md               # This file
```

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.12+
- Node.js 18+
- Git

### Backend Setup
```bash
# Clone the repository
git clone https://github.com/VishalYadav108/ArtWala.git
cd ArtWala

# Set up Django backend
cd artwala_backend
pip install django djangorestframework django-cors-headers
python manage.py migrate
python manage.py populate_data  # Load sample data
python manage.py runserver 8000
```

### Frontend Setup
```bash
# Set up React frontend
cd artwala-frontend
npm install
npm start
```

### Access the Application
- **Backend API**: http://localhost:8000/api/
- **Frontend**: http://localhost:3000
- **Django Admin**: http://localhost:8000/admin/

## 📊 API Endpoints

### Products
- `GET /api/products/products/` - List all products
- `GET /api/products/categories/` - Product categories
- `GET /api/products/cart/` - Shopping cart
- `GET /api/products/orders/` - Order history

### Artists
- `GET /api/artists/profiles/` - Artist profiles
- `GET /api/artists/reviews/` - Artist reviews

### Community
- `GET /api/community/posts/` - Forum posts
- `GET /api/community/forums/` - Discussion forums
- `GET /api/community/jobs/` - Job postings

### Chapters
- `GET /api/chapters/chapters/` - City chapters
- `GET /api/chapters/events/` - Chapter events

### Commissions
- `GET /api/commissions/requests/` - Commission requests
- `GET /api/commissions/proposals/` - Artist proposals

## 💾 Database Models

### Core Models
- **User**: Extended Django user model
- **ArtistProfile**: Artist information and portfolio
- **Product**: Artwork details and pricing
- **Category**: Product categorization
- **Chapter**: City-based communities
- **ForumPost**: Community discussions
- **CommissionRequest**: Custom artwork orders

## 🔧 Development

### Running Tests
```bash
# Backend tests
cd artwala_backend
python manage.py test

# Frontend tests
cd artwala-frontend
npm test
```

### Database Management
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Vishal Yadav**
- GitHub: [@VishalYadav108](https://github.com/VishalYadav108)
- Repository: [ArtWala](https://github.com/VishalYadav108/ArtWala)

## 🙏 Acknowledgments

- Django and React communities for excellent documentation
- GitHub Codespaces for development environment
- All open-source contributors who made this project possible

---

⭐ **Star this repository if you found it helpful!**