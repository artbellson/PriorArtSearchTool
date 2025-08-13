#!/usr/bin/env python3
"""
MMSU Prior Art Search Tool
Main application entry point
"""

import os
from app import create_app

# Create application instance  
config_name = os.environ.get('FLASK_ENV') or 'development'
app = create_app(config_name)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
