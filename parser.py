"""
Description: The PDF Document Parsing Module. Handles binary PDF ingestion securely in-memory using PyMuPDF.
Author: Sudeep Varma K
Date: 2026-06-27
"""
import fitz  # PyMuPDF

def extract_pdf_text(pdf_file):
    """Extracts raw text strings layout-by-layout from an uploaded PDF stream."""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text