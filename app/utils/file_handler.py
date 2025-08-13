"""
File Upload and Processing Utility
"""

import os
import magic
from werkzeug.utils import secure_filename
from flask import current_app
import docx
import PyPDF2
from docx import Document

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file_type(file_path):
    """Validate file type using python-magic"""
    try:
        mime = magic.Magic(mime=True)
        file_mime = mime.from_file(file_path)

        allowed_mimes = {
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        }

        return file_mime in allowed_mimes
    except Exception:
        return False

def extract_text_from_file(file_path):
    """Extract text content from uploaded files"""
    try:
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == '.pdf':
            return extract_text_from_pdf(file_path)
        elif file_extension in ['.doc', '.docx']:
            return extract_text_from_word(file_path)
        else:
            return ""

    except Exception as e:
        current_app.logger.error(f"Text extraction failed: {str(e)}")
        return ""

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"

    except Exception as e:
        current_app.logger.error(f"PDF text extraction failed: {str(e)}")

    return text.strip()

def extract_text_from_word(file_path):
    """Extract text from Word document"""
    text = ""
    try:
        doc = Document(file_path)

        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"

    except Exception as e:
        current_app.logger.error(f"Word text extraction failed: {str(e)}")

    return text.strip()
