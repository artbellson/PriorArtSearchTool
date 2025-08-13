"""
Custom Decorators for MMSU Prior Art Search Tool
"""

from functools import wraps
from flask import abort, request, current_app
from flask_login import current_user

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)

        if not current_user.is_admin():
            abort(403)

        return f(*args, **kwargs)

    return decorated_function

def vip_required(f):
    """Decorator to require VIP or Admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)

        if not current_user.is_vip():
            abort(403)

        return f(*args, **kwargs)

    return decorated_function

def api_key_required(f):
    """Decorator to require valid API key"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')

        if not api_key or api_key != current_app.config.get('API_KEY'):
            abort(401)

        return f(*args, **kwargs)

    return decorated_function
