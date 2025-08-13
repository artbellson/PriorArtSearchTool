#!/usr/bin/env python3
"""
MMSU Prior Art Search Tool
Main application entry point
"""

import os
from app import create_app

app = create_app(os.environ.get('FLASK_ENV') or 'production')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
