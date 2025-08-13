"""
Statistics and Analytics Utility
"""

from datetime import datetime, timedelta
from sqlalchemy import func, and_
from app import db
from app.models import User, TechnologySubmission, CreditHistory, AuditLog

def get_dashboard_stats():
    """Get comprehensive dashboard statistics"""

    # User statistics
    total_users = User.query.count()
    active_users = User.query.filter_by(status='Active').count()
    pending_users = User.query.filter_by(status='Pending').count()
    vip_users = User.query.filter_by(role='VIP').count()
    admin_users = User.query.filter_by(role='Admin').count()

    # Submission statistics
    total_submissions = TechnologySubmission.query.count()
    completed_analyses = TechnologySubmission.query.filter_by(analysis_status='Completed').count()
    pending_analyses = TechnologySubmission.query.filter_by(analysis_status='Pending').count()

    # Time-based statistics
    today = datetime.utcnow().date()
    week_ago = datetime.utcnow() - timedelta(days=7)
    month_ago = datetime.utcnow() - timedelta(days=30)

    submissions_today = TechnologySubmission.query.filter(
        func.date(TechnologySubmission.submitted_at) == today
    ).count()

    submissions_this_week = TechnologySubmission.query.filter(
        TechnologySubmission.submitted_at >= week_ago
    ).count()

    new_users_this_week = User.query.filter(
        User.created_at >= week_ago
    ).count()

    return {
        'users': {
            'total': total_users,
            'active': active_users,
            'pending': pending_users,
            'vip': vip_users,
            'admin': admin_users,
            'new_this_week': new_users_this_week
        },
        'submissions': {
            'total': total_submissions,
            'completed': completed_analyses,
            'pending': pending_analyses,
            'today': submissions_today,
            'this_week': submissions_this_week
        }
    }
