"""
Authentication Routes for MMSU Prior Art Search Tool
"""

import random
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse
from app import db
from app.auth import bp
from app.models import User, AuditLog
from app.auth.forms import LoginForm, RegistrationForm, MathCaptchaForm
from app.utils.email import send_registration_notification

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'error')
            return redirect(url_for('auth.login'))

        if user.status != 'Active':
            flash('Your account is not active. Please contact administrator.', 'error')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        user.last_seen = datetime.utcnow()
        db.session.commit()

        # Log the action
        log = AuditLog(
            user_id=user.id,
            action='user_login',
            resource_type='user',
            resource_id=user.id,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        db.session.add(log)
        db.session.commit()

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.dashboard')
        return redirect(next_page)

    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    """User logout"""
    if current_user.is_authenticated:
        # Log the action
        log = AuditLog(
            user_id=current_user.id,
            action='user_logout',
            resource_type='user',
            resource_id=current_user.id,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        db.session.add(log)
        db.session.commit()

    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    # Generate CAPTCHA
    if 'captcha_answer' not in session:
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        session['captcha_num1'] = num1
        session['captcha_num2'] = num2
        session['captcha_answer'] = num1 + num2

    form = RegistrationForm()
    if form.validate_on_submit():
        # Verify CAPTCHA
        try:
            user_answer = int(form.captcha_answer.data)
            if user_answer != session.get('captcha_answer'):
                flash('Incorrect CAPTCHA answer. Please try again.', 'error')
                # Reset CAPTCHA
                session.pop('captcha_answer', None)
                return redirect(url_for('auth.register'))
        except (ValueError, TypeError):
            flash('Invalid CAPTCHA answer. Please enter a number.', 'error')
            session.pop('captcha_answer', None)
            return redirect(url_for('auth.register'))

        # Create user
        user = User(
            email=form.email.data,
            name=form.name.data,
            institution=form.institution.data,
            phone=form.phone.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        # Clear CAPTCHA from session
        session.pop('captcha_answer', None)
        session.pop('captcha_num1', None)
        session.pop('captcha_num2', None)

        # Send notification to admin
        send_registration_notification(user)

        # Log the action
        log = AuditLog(
            action='user_registration',
            resource_type='user',
            resource_id=user.id,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        log.set_details({'email': user.email, 'name': user.name})
        db.session.add(log)
        db.session.commit()

        flash('Registration successful! Please wait for admin approval.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', 
                         title='Register',
                         form=form,
                         captcha_num1=session.get('captcha_num1'),
                         captcha_num2=session.get('captcha_num2'))
