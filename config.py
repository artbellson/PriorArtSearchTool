"""
MMSU Prior Art Search Tool
Configuration Settings
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or         'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File Upload Configuration
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'artbellsonmamuri@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'eduh lvca meir asmy'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'artbellsonmamuri@gmail.com'

    # Perplexity API Configuration
    PERPLEXITY_API_KEY = os.environ.get('PERPLEXITY_API_KEY')
    PERPLEXITY_API_URL = 'https://api.perplexity.ai/chat/completions'

    # Application Settings
    POSTS_PER_PAGE = 25
    LANGUAGES = ['en', 'es']

    # Credit System
    DEFAULT_CREDITS = 50
    ANALYSIS_COST = 1
    PDF_DOWNLOAD_COST = 1

    # CAPTCHA Settings
    CAPTCHA_TIMEOUT = 600  # 10 minutes

    # WeasyPrint Settings
    WEASYPRINT_BASE_URL = os.environ.get('WEASYPRINT_BASE_URL') or 'http://localhost:5000'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or         'sqlite:///' + os.path.join(basedir, 'app-dev.db')

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or         'sqlite:///' + os.path.join(basedir, 'app.db')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
