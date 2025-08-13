"""
Admin Forms
"""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, Optional

class UserApprovalForm(FlaskForm):
    """Form for approving/rejecting users"""
    action = SelectField('Action', choices=[('approve', 'Approve'), ('reject', 'Reject')])
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Execute')

class CreditAdjustmentForm(FlaskForm):
    """Form for adjusting user credits"""
    action = SelectField('Action', choices=[('add', 'Add Credits'), ('deduct', 'Deduct Credits')])
    adjustment = IntegerField('Amount', validators=[DataRequired(), NumberRange(min=1, max=1000)])
    reason = StringField('Reason', validators=[DataRequired(), Length(min=5, max=200)])
    submit = SubmitField('Adjust Credits')

class EmailBroadcastForm(FlaskForm):
    """Form for sending broadcast emails"""
    recipient_type = SelectField('Recipients', 
                                choices=[('all', 'All Users'), 
                                        ('active', 'Active Users'),
                                        ('vip', 'VIP Users'),
                                        ('regular', 'Regular Users')])
    subject = StringField('Subject', validators=[DataRequired(), Length(max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=2000)])
    submit = SubmitField('Send Email')
