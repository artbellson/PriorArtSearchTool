"""
MMSU Prior Art Search Tool
Application Factory Pattern
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mail = Mail()
csrf = CSRFProtect()

def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Determine config name
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV') or 'production'
    
    # Load configuration from config dictionary
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    
    # Configure login manager
    login.login_view = 'auth.login'
    login.login_message = 'Please log in to access this page.'
    login.login_message_category = 'info'

    # Register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Configure logging
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/mmsu_prior_art.log',
                                         maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('MMSU Prior Art Search Tool startup')

    return app

from app import models
