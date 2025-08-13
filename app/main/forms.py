"""
Forms for Main Blueprint
"""

from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length, Optional
from flask import current_app

class DisclaimerForm(FlaskForm):
    """Technology disclosure disclaimer form"""
    accept_disclaimer = BooleanField(
        'I agree to disclose my technology information for prior art search analysis. '
        'I understand that all disclosed data will be kept confidential and processed by AI for analysis purposes.',
        validators=[DataRequired()]
    )
    submit = SubmitField('I Agree and Continue')

class TechnologySubmissionForm(FlaskForm):
    """Technology submission form"""
    title = StringField('Technology Title', 
                       validators=[DataRequired(), Length(min=5, max=200)],
                       render_kw={"placeholder": "Enter a descriptive title for your technology"})

    description = TextAreaField('Detailed Description',
                               validators=[DataRequired(), Length(min=50, max=5000)],
                               render_kw={"placeholder": "Provide a comprehensive description of your technology, including its purpose, functionality, and key features", "rows": 8})

    claims = TextAreaField('Claims (Optional)',
                          validators=[Optional(), Length(max=3000)],
                          render_kw={"placeholder": "List the specific claims or novel aspects of your technology", "rows": 6})

    inventors = StringField('Inventor(s) (Optional)',
                           validators=[Optional(), Length(max=500)],
                           render_kw={"placeholder": "Enter inventor names separated by commas"})

    institution = StringField('Institution (Optional)',
                             validators=[Optional(), Length(max=200)],
                             render_kw={"placeholder": "Institution or organization name"})

    uploaded_file = FileField('Upload File (Optional)',
                             validators=[Optional(), 
                                       FileAllowed(['pdf', 'doc', 'docx'], 
                                                 'Only PDF, DOC, and DOCX files are allowed')])

    submit = SubmitField('Submit for Analysis')

class MathCaptchaForm(FlaskForm):
    """Simple math CAPTCHA form"""
    captcha_answer = StringField('Answer', validators=[DataRequired()])
    submit = SubmitField('Verify')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        import random
        self.num1 = random.randint(1, 10)
        self.num2 = random.randint(1, 10)
        self.correct_answer = self.num1 + self.num2

    def validate_captcha_answer(self, field):
        try:
            answer = int(field.data)
            if answer != self.correct_answer:
                raise ValidationError('Incorrect answer. Please try again.')
        except ValueError:
            raise ValidationError('Please enter a valid number.')
