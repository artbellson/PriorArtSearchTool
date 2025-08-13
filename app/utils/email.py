"""
Email Utility for MMSU Prior Art Search Tool
"""

from datetime import datetime
from flask import current_app, render_template, url_for
from flask_mail import Message
from app import mail, db
from app.models import EmailLog

def send_email(subject, recipients, template, **kwargs):
    """Send email with template"""
    try:
        # Render email templates
        html_body = render_template(f'email/{template}.html', **kwargs)
        text_body = render_template(f'email/{template}.txt', **kwargs)

        # Create message
        msg = Message(
            subject=subject,
            recipients=recipients,
            html=html_body,
            body=text_body,
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )

        # Send email
        mail.send(msg)

        # Log successful send
        for recipient in recipients:
            log_email_sent(recipient, subject, template, 'Sent')

        return True

    except Exception as e:
        current_app.logger.error(f"Email sending failed: {str(e)}")

        # Log failed send
        for recipient in recipients:
            log_email_failed(recipient, subject, template, str(e))

        return False

def send_registration_notification(user):
    """Send registration notification to admin"""
    from app.models import User
    admin_users = User.query.filter_by(role='Admin').all()
    admin_emails = [admin.email for admin in admin_users]

    if admin_emails:
        send_email(
            subject=f'New User Registration - {user.name}',
            recipients=admin_emails,
            template='admin_new_registration',
            user=user,
            admin_url=current_app.config.get('ADMIN_URL', 'https://your-app.com/admin')
        )

def send_approval_notification(user):
    """Send approval notification to user"""
    send_email(
        subject='MMSU Prior Art Search - Account Approved',
        recipients=[user.email],
        template='user_approved',
        user=user,
        app_url=current_app.config.get('APP_URL', 'https://your-app.com')
    )

def send_rejection_notification(user):
    """Send rejection notification to user"""
    send_email(
        subject='MMSU Prior Art Search - Registration Update',
        recipients=[user.email],
        template='user_rejected',
        user=user
    )

def log_email_sent(recipient, subject, template, status):
    """Log email sending attempt"""
    log = EmailLog(
        recipient_email=recipient,
        subject=subject,
        template_name=template,
        status=status,
        sent_at=datetime.utcnow()
    )
    db.session.add(log)
    db.session.commit()

def log_email_failed(recipient, subject, template, error_message):
    """Log failed email sending"""
    log = EmailLog(
        recipient_email=recipient,
        subject=subject,
        template_name=template,
        status='Failed',
        error_message=error_message
    )
    db.session.add(log)
    db.session.commit()
