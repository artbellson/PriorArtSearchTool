#!/usr/bin/env python3
"""
WSGI entry point for production deployment
"""

import os
from app import create_app

# Create application instance
config_name = os.environ.get('FLASK_ENV') or 'production'
application = create_app(config_name)

if __name__ == "__main__":
    application.run()
