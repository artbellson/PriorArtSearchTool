"""
PDF Report Generation Utility using WeasyPrint
"""

import os
import tempfile
from datetime import datetime
from flask import render_template, current_app
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

def generate_pdf_report(submission):
    """Generate PDF report for technology submission"""

    # Get analysis results
    results = submission.get_results()

    if not results:
        raise ValueError("No analysis results available for PDF generation")

    # Prepare data for template
    template_data = {
        'submission': submission,
        'results': results,
        'generated_date': datetime.utcnow().strftime('%B %d, %Y at %I:%M %p UTC'),
        'university_info': {
            'name': 'Mariano Marcos State University',
            'address': 'Brgy. 16-S Quiling Sur, City of Batac, Ilocos Norte, Philippines 2906',
            'contact': 'op@mmsu.edu.ph | (63)(77) 670-4089'
        },
        'signature_info': {
            'name': 'Engr. Artbellson B. Mamuri',
            'title': 'Chief UITSO',
            'contact': '09482920644'
        }
    }

    # Render HTML template
    html_content = render_template('pdf/report_template.html', **template_data)

    # Create CSS for PDF styling
    css_content = get_pdf_css()

    # Generate PDF
    font_config = FontConfiguration()

    # Create temporary file for PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        pdf_path = tmp_file.name

    try:
        # Generate PDF with WeasyPrint
        HTML(string=html_content, base_url=current_app.config.get('WEASYPRINT_BASE_URL')).write_pdf(
            pdf_path,
            stylesheets=[CSS(string=css_content, font_config=font_config)],
            font_config=font_config
        )

        return pdf_path

    except Exception as e:
        # Clean up temp file on error
        if os.path.exists(pdf_path):
            os.unlink(pdf_path)
        raise RuntimeError(f"PDF generation failed: {str(e)}")

def get_pdf_css():
    """Get CSS styling for PDF generation"""
    return """
    @page {
        size: A4;
        margin: 2cm 1.5cm 2cm 1.5cm;
        @top-center {
            content: "MMSU Prior Art Search Report - Confidential";
            font-size: 10pt;
            color: #666;
            font-family: Inter, sans-serif;
        }
        @bottom-center {
            content: "Page " counter(page) " of " counter(pages);
            font-size: 10pt;
            color: #666;
            font-family: Inter, sans-serif;
        }
    }

    body {
        font-family: Inter, 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 11pt;
        line-height: 1.6;
        color: #333;
        margin: 0;
        padding: 0;
    }

    .header {
        text-align: center;
        margin-bottom: 30px;
        border-bottom: 3px solid #006400;
        padding-bottom: 20px;
    }

    .university-name {
        font-size: 18pt;
        font-weight: bold;
        color: #006400;
        margin-bottom: 5px;
    }

    .report-title {
        font-size: 16pt;
        font-weight: 600;
        color: #333;
        margin-bottom: 10px;
    }

    .serial-number {
        background: #FFC107;
        color: #000;
        padding: 5px 10px;
        border-radius: 4px;
        font-weight: bold;
        display: inline-block;
        margin-top: 10px;
    }

    .section {
        margin: 25px 0;
        page-break-inside: avoid;
    }

    .section-title {
        font-size: 14pt;
        font-weight: bold;
        color: #006400;
        border-bottom: 2px solid #006400;
        padding-bottom: 5px;
        margin-bottom: 15px;
    }

    .disclaimer {
        background: #ffebee;
        border: 2px solid #c62828;
        border-radius: 6px;
        padding: 20px;
        margin: 30px 0;
        page-break-inside: avoid;
    }

    .disclaimer-title {
        font-size: 14pt;
        font-weight: bold;
        color: #c62828;
        margin-bottom: 10px;
        text-align: center;
    }

    .footer {
        margin-top: 40px;
        border-top: 1px solid #ddd;
        padding-top: 20px;
        text-align: center;
        color: #666;
        font-size: 10pt;
    }
    """
