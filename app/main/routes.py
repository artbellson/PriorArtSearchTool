"""
Main Routes for MMSU Prior Art Search Tool
"""

import os
import json
import uuid
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app, jsonify, send_file
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from app import db
from app.main import bp
from app.models import User, TechnologySubmission, CreditHistory, DownloadHistory, AuditLog
from app.main.forms import TechnologySubmissionForm, DisclaimerForm
from app.utils.ai_analysis import PerplexityAnalyzer
from app.utils.pdf_generator import generate_pdf_report
from app.utils.file_handler import allowed_file, extract_text_from_file

@bp.route('/')
@bp.route('/index')
def index():
    """Landing page"""
    return render_template('main/index.html', title='MMSU Prior Art Search Tool')

@bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    # Check if user needs to accept disclaimer
    if not current_user.disclaimer_accepted:
        return redirect(url_for('main.disclaimer'))

    # Get user's recent submissions
    submissions = current_user.submissions.order_by(
        TechnologySubmission.submitted_at.desc()
    ).limit(10).all()

    # Get recent credit history
    credit_history = current_user.credit_history.order_by(
        CreditHistory.created_at.desc()
    ).limit(10).all()

    return render_template('main/dashboard.html', 
                         title='Dashboard',
                         submissions=submissions,
                         credit_history=credit_history)

@bp.route('/disclaimer', methods=['GET', 'POST'])
@login_required
def disclaimer():
    """Technology disclosure disclaimer page"""
    if current_user.disclaimer_accepted:
        return redirect(url_for('main.dashboard'))

    form = DisclaimerForm()
    if form.validate_on_submit():
        if form.accept_disclaimer.data:
            current_user.disclaimer_accepted = True
            current_user.disclaimer_accepted_at = datetime.utcnow()
            db.session.commit()

            # Log the action
            log_audit_action('disclaimer_accepted', 'user', current_user.id)

            flash('Disclaimer accepted. You can now proceed to submit technologies.', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('You must accept the disclaimer to continue.', 'error')

    return render_template('main/disclaimer.html', title='Disclaimer', form=form)

@bp.route('/submit', methods=['GET', 'POST'])
@login_required
def submit_technology():
    """Technology submission form"""
    if not current_user.disclaimer_accepted:
        return redirect(url_for('main.disclaimer'))

    # Check if user has credits
    if not current_user.has_credits():
        flash('Insufficient credits. Please contact administrator or upgrade to VIP.', 'error')
        return redirect(url_for('main.dashboard'))

    form = TechnologySubmissionForm()
    if form.validate_on_submit():
        # Handle file upload
        uploaded_file = None
        file_content = ""

        if form.uploaded_file.data:
            file = form.uploaded_file.data
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to filename to avoid conflicts
                filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                uploaded_file = filename

                # Extract text from file
                file_content = extract_text_from_file(filepath)
            else:
                flash('Invalid file type. Only PDF, DOC, and DOCX files are allowed.', 'error')
                return render_template('main/submit.html', title='Submit Technology', form=form)

        # Create submission
        submission = TechnologySubmission(
            title=form.title.data,
            description=form.description.data,
            claims=form.claims.data,
            inventors=form.inventors.data,
            institution=form.institution.data or current_user.institution,
            uploaded_file=uploaded_file,
            file_content=file_content,
            user_id=current_user.id
        )
        submission.generate_serial_number()

        db.session.add(submission)
        db.session.commit()

        # Deduct credits
        current_user.deduct_credits(current_app.config.get('ANALYSIS_COST', 1))

        # Record credit transaction
        credit_record = CreditHistory(
            user_id=current_user.id,
            submission_id=submission.id,
            transaction_type='analysis',
            amount=-current_app.config.get('ANALYSIS_COST', 1),
            balance_after=current_user.credits,
            description=f'Analysis for: {submission.title[:50]}...'
        )
        db.session.add(credit_record)
        db.session.commit()

        # Log the action
        log_audit_action('submission_created', 'submission', submission.id, {
            'title': submission.title,
            'has_file': uploaded_file is not None
        })

        flash('Technology submitted successfully! Analysis is in progress.', 'success')
        return redirect(url_for('main.analyze', id=submission.id))

    return render_template('main/submit.html', title='Submit Technology', form=form)

@bp.route('/analyze/<int:id>')
@login_required
def analyze(id):
    """AI analysis processing page"""
    submission = TechnologySubmission.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    if submission.analysis_status == 'Completed':
        return redirect(url_for('main.results', id=id))

    # Simulate AI analysis (in production, this would be async)
    if submission.analysis_status == 'Pending':
        submission.analysis_status = 'Processing'
        db.session.commit()

        # Perform AI analysis
        analyzer = PerplexityAnalyzer()
        results = analyzer.analyze_technology(submission)

        submission.set_results(results)
        submission.analysis_status = 'Completed'
        submission.analyzed_at = datetime.utcnow()
        db.session.commit()

        # Log the action
        log_audit_action('analysis_completed', 'submission', submission.id)

    return render_template('main/analyze.html', title='AI Analysis', submission=submission)

@bp.route('/results/<int:id>')
@login_required
def results(id):
    """Display analysis results"""
    submission = TechnologySubmission.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    if submission.analysis_status != 'Completed':
        return redirect(url_for('main.analyze', id=id))

    results = submission.get_results()

    return render_template('main/results.html', 
                         title='Analysis Results',
                         submission=submission,
                         results=results)

@bp.route('/download_pdf/<int:id>')
@login_required
def download_pdf(id):
    """Download PDF report"""
    submission = TechnologySubmission.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    if submission.analysis_status != 'Completed':
        flash('Analysis not completed yet.', 'error')
        return redirect(url_for('main.results', id=id))

    # Check credits for non-VIP users
    if not current_user.is_vip() and not current_user.has_credits():
        flash('Insufficient credits for PDF download.', 'error')
        return redirect(url_for('main.results', id=id))

    # Deduct credits for PDF download
    if not current_user.is_vip():
        current_user.deduct_credits(current_app.config.get('PDF_DOWNLOAD_COST', 1))

        # Record credit transaction
        credit_record = CreditHistory(
            user_id=current_user.id,
            submission_id=submission.id,
            transaction_type='download',
            amount=-current_app.config.get('PDF_DOWNLOAD_COST', 1),
            balance_after=current_user.credits,
            description=f'PDF download for: {submission.title[:50]}...'
        )
        db.session.add(credit_record)
        db.session.commit()

    # Record download
    download_record = DownloadHistory(
        user_id=current_user.id,
        submission_id=submission.id,
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string
    )
    db.session.add(download_record)
    db.session.commit()

    # Generate PDF
    pdf_file = generate_pdf_report(submission)

    # Log the action
    log_audit_action('pdf_downloaded', 'submission', submission.id)

    return send_file(pdf_file, as_attachment=True, 
                    download_name=f"MMSU_Prior_Art_Report_{submission.serial_number}.pdf")

@bp.route('/history')
@login_required
def history():
    """View submission history"""
    page = request.args.get('page', 1, type=int)
    submissions = current_user.submissions.order_by(
        TechnologySubmission.submitted_at.desc()
    ).paginate(page=page, per_page=current_app.config.get('POSTS_PER_PAGE', 25), 
              error_out=False)

    return render_template('main/history.html', 
                         title='Submission History',
                         submissions=submissions)

def log_audit_action(action, resource_type, resource_id, details=None):
    """Helper function to log audit actions"""
    log = AuditLog(
        user_id=current_user.id if current_user.is_authenticated else None,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string
    )
    if details:
        log.set_details(details)
    db.session.add(log)
    db.session.commit()
