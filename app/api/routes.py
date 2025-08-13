"""
API Routes for MMSU Prior Art Search Tool
"""

from flask import jsonify, request, current_app
from flask_login import login_required, current_user
from app.api import bp
from app.models import User, TechnologySubmission, CreditHistory
from app.utils.decorators import api_key_required

@bp.route('/status')
def status():
    """API status check"""
    return jsonify({
        'status': 'ok',
        'message': 'MMSU Prior Art Search Tool API is running'
    })

@bp.route('/user/profile')
@login_required
def user_profile():
    """Get current user profile"""
    return jsonify({
        'id': current_user.id,
        'name': current_user.name,
        'email': current_user.email,
        'role': current_user.role,
        'credits': current_user.credits,
        'status': current_user.status,
        'institution': current_user.institution,
        'created_at': current_user.created_at.isoformat(),
        'disclaimer_accepted': current_user.disclaimer_accepted
    })

@bp.route('/user/submissions')
@login_required
def user_submissions():
    """Get user's submissions"""
    submissions = current_user.submissions.order_by(
        TechnologySubmission.submitted_at.desc()
    ).all()

    return jsonify({
        'submissions': [
            {
                'id': sub.id,
                'title': sub.title,
                'status': sub.analysis_status,
                'submitted_at': sub.submitted_at.isoformat(),
                'analyzed_at': sub.analyzed_at.isoformat() if sub.analyzed_at else None,
                'serial_number': sub.serial_number
            } for sub in submissions
        ]
    })
