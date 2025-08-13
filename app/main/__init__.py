"""
Main Blueprint for MMSU Prior Art Search Tool
"""

from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes
