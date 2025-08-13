#!/usr/bin/env python3
"""
WSGI entry point for production deployment
"""

import os
from app import create_app

# Create application instance
application = create_app(os.environ.get('FLASK_ENV') or 'production')

if __name__ == "__main__":
    application.run()
