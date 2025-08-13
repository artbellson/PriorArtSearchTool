"""
Admin Routes for MMSU Prior Art Search Tool
"""

from datetime import datetime, timedelta
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.admin import bp
from app.models import User, TechnologySubmission, CreditHistory, AuditLog, EmailLog
from app.admin.forms import UserApprovalForm, CreditAdjustmentForm, EmailBroadcastForm
from app.utils.decorators import admin_required
from app.utils.email import send_approval_notification, send_rejection_notification
from app.utils.statistics import get_dashboard_stats

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard"""
    stats = get_dashboard_stats()

    # Get recent activities
    recent_registrations = User.query.filter_by(status='Pending').order_by(
        User.created_at.desc()).limit(5).all()

    recent_submissions = TechnologySubmission.query.order_by(
        TechnologySubmission.submitted_at.desc()).limit(10).all()

    recent_logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(10).all()

    return render_template('admin/dashboard.html',
                         title='Admin Dashboard',
                         stats=stats,
                         recent_registrations=recent_registrations,
                         recent_submissions=recent_submissions,
                         recent_logs=recent_logs)

@bp.route('/users')
@login_required
@admin_required
def users():
    """User management"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'all')
    role_filter = request.args.get('role', 'all')

    query = User.query

    if status_filter != 'all':
        query = query.filter_by(status=status_filter)

    if role_filter != 'all':
        query = query.filter_by(role=role_filter)

    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=25, error_out=False)

    return render_template('admin/users.html',
                         title='User Management',
                         users=users,
                         status_filter=status_filter,
                         role_filter=role_filter)

@bp.route('/approve_user/<int:id>')
@login_required
@admin_required
def approve_user(id):
    """Approve user registration"""
    user = User.query.get_or_404(id)

    if user.status != 'Pending':
        flash(f'User {user.name} is not pending approval.', 'error')
        return redirect(url_for('admin.users'))

    user.status = 'Active'
    db.session.commit()

    # Send approval notification
    send_approval_notification(user)

    # Log the action
    log = AuditLog(
        user_id=current_user.id,
        action='user_approved',
        resource_type='user',
        resource_id=user.id,
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string
    )
    log.set_details({'approved_user_email': user.email})
    db.session.add(log)
    db.session.commit()

    flash(f'User {user.name} has been approved.', 'success')
    return redirect(url_for('admin.users'))
