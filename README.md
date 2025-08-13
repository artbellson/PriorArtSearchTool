# MMSU Prior Art Search Tool

## AI-Powered Prior Art Search System for Mariano Marcos State University

A comprehensive, production-ready Flask web application that provides AI-powered prior art search and patentability analysis for MMSU researchers, faculty, and students.

### 🎯 Features

#### Core Functionality
- **AI-Powered Analysis**: Integration with Perplexity API for comprehensive prior art search
- **Technology Submission**: User-friendly form for technology disclosure
- **Patentability Assessment**: Analysis of novelty, inventive step, and industrial applicability
- **Professional Reports**: PDF generation with MMSU branding and confidentiality notes
- **Credit Management**: Flexible credit system with usage tracking

#### User Management
- **Three User Roles**: Admin (unlimited), VIP (unlimited), Regular (50 credits)
- **Admin Approval**: Registration requires administrative approval
- **Math CAPTCHA**: Simple anti-bot protection during registration
- **Audit Logging**: Comprehensive activity tracking

#### Admin Dashboard
- **User Management**: Approve/deny registrations, manage roles and credits
- **Analytics**: Usage statistics, submission tracking, system health
- **Email System**: Automated notifications and broadcast capabilities
- **Audit Trail**: Complete logging of all system activities

#### Security & Compliance
- **Confidentiality Agreements**: Mandatory disclaimer acceptance
- **Input Validation**: Protection against XSS and SQL injection
- **Secure File Upload**: Support for PDF, DOC, and DOCX files
- **Email Notifications**: HTML templates with professional signatures

### 🛠 Technology Stack

- **Backend**: Flask 3.1.0 with Blueprint architecture
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Frontend**: Bootstrap 5 with MMSU branding and dark mode
- **PDF Generation**: WeasyPrint for professional reports
- **Email**: Flask-Mail with Gmail SMTP integration
- **AI Integration**: Perplexity API for prior art analysis
- **Deployment**: Render.com with Gunicorn production server

### 🚀 Quick Start

#### Prerequisites
- Python 3.11.5+
- PostgreSQL (for production) or SQLite (for development)
- Git
- Render.com account (for deployment)

#### Local Development Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repo/mmsu-prior-art-tool.git
   cd mmsu-prior-art-tool
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` file with your configuration:
   ```env
   SECRET_KEY=your-secret-key-here
   FLASK_ENV=development
   DATABASE_URL=sqlite:///app.db
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   PERPLEXITY_API_KEY=your-perplexity-api-key
   ```

5. **Initialize Database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Create Admin User**
   ```bash
   flask shell
   ```
   ```python
   from app import db
   from app.models import User

   admin = User(
       email='admin@mmsu.edu.ph',
       name='Admin User',
       role='Admin',
       status='Active',
       disclaimer_accepted=True
   )
   admin.set_password('admin123')
   db.session.add(admin)
   db.session.commit()
   ```

7. **Run Development Server**
   ```bash
   flask run
   ```

   Visit `http://localhost:5000` to access the application.

### 🌐 Production Deployment on Render.com

#### Automated Deployment

1. **Fork/Clone to GitHub**
   - Fork this repository to your GitHub account
   - Ensure all files are committed and pushed

2. **Connect to Render**
   - Log in to [Render.com](https://render.com)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file

3. **Configure Environment Variables**
   Set these environment variables in Render dashboard:
   ```
   MAIL_PASSWORD=your-gmail-app-password
   PERPLEXITY_API_KEY=your-perplexity-api-key
   ```

4. **Deploy**
   - Click "Deploy" and wait for the build to complete
   - Your app will be live at `https://your-app-name.onrender.com`

### 📁 Project Structure

```
mmsu_prior_art_tool/
├── app/                          # Main application package
│   ├── __init__.py              # Application factory
│   ├── models.py                # Database models
│   ├── admin/                   # Admin blueprint
│   ├── auth/                    # Authentication blueprint
│   ├── main/                    # Main application blueprint
│   ├── api/                     # API blueprint
│   ├── static/                  # Static assets
│   ├── templates/               # Jinja2 templates
│   ├── uploads/                 # File uploads
│   └── utils/                   # Utility modules
├── migrations/                  # Database migrations
├── tests/                      # Test suite
├── app.py                      # Application entry point
├── wsgi.py                     # WSGI entry point
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── render.yaml                 # Render deployment config
└── README.md                  # This file
```

### 🔧 Configuration

#### Default Admin Account
- **Email**: admin@mmsu.edu.ph
- **Password**: admin123
- **Role**: Admin

⚠️ **Important**: Change the default admin password immediately after deployment.

#### MMSU Branding
The application uses official MMSU colors and branding:
- **Deep Green**: #006400
- **Gold**: #FFC107
- **Charcoal**: #343A40
- **Light Gray**: #F8F9FA

#### Credit System
- **Regular Users**: Start with 50 credits
- **Analysis Cost**: 1 credit per submission
- **PDF Download**: 1 credit per download
- **VIP/Admin**: Unlimited credits

### 📧 Email Configuration

#### Gmail SMTP Setup
1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account Settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. Use the generated password in `MAIL_PASSWORD` environment variable

### 🔑 API Integration

#### Perplexity API Setup
1. Sign up at [Perplexity.ai](https://www.perplexity.ai)
2. Get API key from dashboard
3. Set `PERPLEXITY_API_KEY` in environment variables

### 📞 Support

#### Contact Information
- **Developer**: MMSU UITSO Team
- **Email**: op@mmsu.edu.ph
- **Phone**: (63)(77) 670-4089

#### MMSU Information
- **University**: Mariano Marcos State University
- **Vision**: A premier Philippine university by 2028
- **Mission**: To develop virtuous human capital and sustainable innovations in a knowledge-driven global economy

### 📄 License

This project is proprietary software developed for Mariano Marcos State University. All rights reserved.

---

**Made with ❤️ for MMSU by the UITSO Team**

*Engr. Artbellson B. Mamuri, Chief UITSO*  
*Contact: 09482920644*
