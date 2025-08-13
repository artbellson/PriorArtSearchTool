"""
Admin Blueprint for MMSU Prior Art Search Tool
"""

from flask import Blueprint

bp = Blueprint('admin', __name__)

from app.admin import routes
