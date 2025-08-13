"""
MMSU Prior Art Search Tool
Database Models
"""

from datetime import datetime, timedelta
import json
from hashlib import md5
from time import time
from flask import current_app, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login

class User(UserMixin, db.Model):
    """User model"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128))
    institution = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), default='Regular')  # Admin, VIP, Regular
    credits = db.Column(db.Integer, default=50)
    status = db.Column(db.String(20), default='Pending')  # Pending, Active, Inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    disclaimer_accepted = db.Column(db.Boolean, default=False)
    disclaimer_accepted_at = db.Column(db.DateTime)

    # Relationships
    submissions = db.relationship('TechnologySubmission', backref='author', lazy='dynamic')
    credit_history = db.relationship('CreditHistory', backref='user', lazy='dynamic')
    audit_logs = db.relationship('AuditLog', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256'
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                          algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def has_credits(self, amount=1):
        """Check if user has enough credits"""
        if self.role in ['Admin', 'VIP']:
            return True
        return self.credits >= amount

    def deduct_credits(self, amount):
        """Deduct credits from user account"""
        if self.role not in ['Admin', 'VIP']:
            self.credits -= amount
            if self.credits < 0:
                self.credits = 0

    def add_credits(self, amount):
        """Add credits to user account"""
        if self.role not in ['Admin', 'VIP']:
            self.credits += amount

    def is_admin(self):
        return self.role == 'Admin'

    def is_vip(self):
        return self.role in ['Admin', 'VIP']

class TechnologySubmission(db.Model):
    """Technology submission model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    claims = db.Column(db.Text)
    inventors = db.Column(db.String(500))
    institution = db.Column(db.String(200))
    uploaded_file = db.Column(db.String(200))
    file_content = db.Column(db.Text)  # Extracted text from uploaded files

    # Analysis results
    analysis_status = db.Column(db.String(20), default='Pending')  # Pending, Processing, Completed, Failed
    analysis_results = db.Column(db.Text)  # JSON string of results
    serial_number = db.Column(db.String(50), unique=True)

    # Timestamps
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    analyzed_at = db.Column(db.DateTime)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    downloads = db.relationship('DownloadHistory', backref='submission', lazy='dynamic')

    def __repr__(self):
        return f'<Submission {self.title}>'

    def get_results(self):
        """Get analysis results as Python object"""
        if self.analysis_results:
            return json.loads(self.analysis_results)
        return None

    def set_results(self, results):
        """Set analysis results from Python object"""
        self.analysis_results = json.dumps(results)

    def generate_serial_number(self):
        """Generate unique serial number for the submission"""
        import uuid
        self.serial_number = f"MMSU-PA-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"

class CreditHistory(db.Model):
    """Credit transaction history"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    submission_id = db.Column(db.Integer, db.ForeignKey('technology_submission.id'))
    transaction_type = db.Column(db.String(20), nullable=False)  # analysis, download, adjustment, grant
    amount = db.Column(db.Integer, nullable=False)  # Negative for deductions, positive for additions
    balance_after = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CreditHistory {self.transaction_type}: {self.amount}>'

class DownloadHistory(db.Model):
    """PDF download history"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    submission_id = db.Column(db.Integer, db.ForeignKey('technology_submission.id'), nullable=False)
    download_type = db.Column(db.String(20), default='pdf')
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    downloaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref='downloads')

class AuditLog(db.Model):
    """Audit log for tracking all system activities"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    action = db.Column(db.String(100), nullable=False)
    resource_type = db.Column(db.String(50))
    resource_id = db.Column(db.Integer)
    details = db.Column(db.Text)  # JSON string with additional details
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<AuditLog {self.action}>'

    def get_details(self):
        """Get details as Python object"""
        if self.details:
            return json.loads(self.details)
        return {}

    def set_details(self, details):
        """Set details from Python object"""
        self.details = json.dumps(details)

class EmailLog(db.Model):
    """Email sending log"""
    id = db.Column(db.Integer, primary_key=True)
    recipient_email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    template_name = db.Column(db.String(50))
    status = db.Column(db.String(20), default='Pending')  # Pending, Sent, Failed
    error_message = db.Column(db.Text)
    sent_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<EmailLog {self.recipient_email}: {self.subject}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
