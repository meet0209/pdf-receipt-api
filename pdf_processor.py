import pdfplumber
import PyPDF2
from io import BytesIO
import re

def clean_duplicate_chars(text):
    """
    Clean duplicate characters from PDF extraction
    This PDF specifically repeats each character exactly 4 times:
    - 'RRRRMMMM' → 'RM'
    - '111100000000' → '100'
    - '....' → '.'
    
    Args:
        text (str): Text with 4x character repetitions
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return text
    
    # This PDF repeats each character EXACTLY 4 times
    # Strategy: Take every 4th character
    result = []
    i = 0
    
    while i < len(text):
        char = text[i]
        
        # Check if this character is repeated 4 times
        if i + 3 < len(text) and all(text[i+j] == char for j in range(4)):
            # Yes, it's repeated 4 times - take it once
            result.append(char)
            i += 4  # Skip the next 3 duplicates
        else:
            # No pattern - keep as is
            result.append(char)
            i += 1
    
    return ''.join(result)

def extract_pdf_data(file):
    """
    Extract text from PDF using multiple methods
    
    Args:
        file: FileStorage object from Flask request
        
    Returns:
        str: Extracted text from PDF
        
    Raises:
        Exception: If unable to extract text from PDF
    """
    text = ""
    
    try:
        # Method 1: Try pdfplumber (works best for text-based PDFs)
        print("Attempting pdfplumber extraction...")
        file.seek(0)
        with pdfplumber.open(file) as pdf:
            page_count = len(pdf.pages)
            print(f"PDF has {page_count} page(s)")
            
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                    print(f"Page {i+1}: Extracted {len(page_text)} characters")
        
        # If text extracted successfully, clean and return it
        if text.strip():
            print(f"✅ pdfplumber succeeded - Total: {len(text)} characters")
            cleaned_text = clean_duplicate_chars(text)
            print(f"🧹 Cleaned text - Total: {len(cleaned_text)} characters")
            return cleaned_text
        else:
            print("⚠️ pdfplumber extracted no text")
        
    except Exception as e:
        print(f"❌ pdfplumber failed: {e}")
    
    try:
        # Method 2: Try PyPDF2 (fallback)
        print("Attempting PyPDF2 extraction...")
        file.seek(0)
        pdf_reader = PyPDF2.PdfReader(file)
        page_count = len(pdf_reader.pages)
        print(f"PDF has {page_count} page(s)")
        
        for i, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
                print(f"Page {i+1}: Extracted {len(page_text)} characters")
        
        if text.strip():
            print(f"✅ PyPDF2 succeeded - Total: {len(text)} characters")
            cleaned_text = clean_duplicate_chars(text)
            print(f"🧹 Cleaned text - Total: {len(cleaned_text)} characters")
            return cleaned_text
        else:
            print("⚠️ PyPDF2 extracted no text")
            
    except Exception as e:
        print(f"❌ PyPDF2 failed: {e}")
    
    # If we reach here, no method worked
    if not text.strip():
        raise Exception(
            "Could not extract text from PDF. "
            "The PDF might be image-based (scanned) or corrupted. "
            "Please ensure the PDF contains selectable text."
        )
    
    return text
