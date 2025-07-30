import PyPDF2
import re
import os
import tempfile
from datetime import datetime
from typing import Optional
from .schemas import PatientInfo

# OCR imports
try:
    import pytesseract
    from pdf2image import convert_from_bytes
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("OCR libraries not available. Install pytesseract, pdf2image, and Pillow for OCR support.")

def extract_patient_info_from_pdf(pdf_content: bytes) -> Optional[PatientInfo]:
    """
    Extract patient information from PDF content.
    Returns PatientInfo object with first_name, last_name, and date_of_birth.
    """
    try:
        # Create a BytesIO object to make bytes file-like
        from io import BytesIO
        pdf_file = BytesIO(pdf_content)
        
        # Create PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Check if PDF is encrypted
        if pdf_reader.is_encrypted:
            print("PDF is encrypted/password protected")
            return None
        
        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # If no text extracted, try OCR for image-based PDFs
        if not text.strip():
            if OCR_AVAILABLE:
                print("📄 No text found in PDF. Using OCR to extract from images...")
                ocr_text = extract_text_with_ocr(pdf_content)
                if ocr_text:
                    print(f"✅ OCR extracted {len(ocr_text)} characters of text")
                    
                    # Extract patient information from OCR text
                    first_name = extract_first_name(ocr_text)
                    last_name = extract_last_name(ocr_text)
                    date_of_birth = extract_date_of_birth(ocr_text)
                    
                    print(f"👤 Extracted Patient Info: {first_name} {last_name}, DOB: {date_of_birth}")
                    
                    if first_name and last_name and date_of_birth:
                        return PatientInfo(
                            first_name=first_name,
                            last_name=last_name,
                            date_of_birth=date_of_birth
                        )
                else:
                    print("❌ OCR failed to extract text from PDF")
            else:
                print("❌ OCR not available. Install tesseract and poppler for image-based PDF support")
            return None
        
        # Extract patient information using regex patterns
        first_name = extract_first_name(text)
        last_name = extract_last_name(text)
        date_of_birth = extract_date_of_birth(text)
        
        if first_name and last_name and date_of_birth:
            return PatientInfo(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth
            )
        
        return None
        
    except Exception as e:
        print(f"Error parsing PDF: {str(e)}")
        return None

def extract_first_name(text: str) -> Optional[str]:
    """Extract first name from text using various patterns."""
    # Look for the specific pattern in your PDF
    specific_pattern = r"Patient Name[^:]*?Patient Date of Birth\s*([A-Z][a-z]+)\s+([A-Z][a-z]+)"
    match = re.search(specific_pattern, text, re.IGNORECASE)
    if match:
        first_name = match.group(1).strip()
        last_name = match.group(2).strip()
        # Filter out common non-name words
        if (first_name.lower() not in ['patient', 'name', 'first', 'last', 'given', 'surname', 'and', 'address'] and
            last_name.lower() not in ['patient', 'name', 'first', 'last', 'given', 'surname', 'and', 'address']):
            return first_name
    
    # Fallback patterns
    patterns = [
        r"Name[:\s]*([A-Z][a-z]+)\s+[A-Z][a-z]+",  # "Name: John Doe"
        r"First Name[:\s]*([A-Za-z]+)",
        r"Given Name[:\s]*([A-Za-z]+)",
        r"Patient First Name[:\s]*([A-Za-z]+)",
        r"First[:\s]*([A-Za-z]+)",
        r"F\.?Name[:\s]*([A-Za-z]+)",
        r"Patient[:\s]*([A-Za-z]+)\s+[A-Za-z]+",  # First word after "Patient:"
        r"([A-Z][a-z]+)\s+[A-Z][a-z]+",  # Two capitalized words (common name pattern)
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            # Filter out common non-name words
            if name.lower() not in ['patient', 'name', 'first', 'last', 'given', 'surname']:
                return name
    
    return None

def extract_last_name(text: str) -> Optional[str]:
    """Extract last name from text using various patterns."""
    # Look for the specific pattern in your PDF
    specific_pattern = r"Patient Name[^:]*?Patient Date of Birth\s*([A-Z][a-z]+)\s+([A-Z][a-z]+)"
    match = re.search(specific_pattern, text, re.IGNORECASE)
    if match:
        first_name = match.group(1).strip()
        last_name = match.group(2).strip()
        # Filter out common non-name words
        if (first_name.lower() not in ['patient', 'name', 'first', 'last', 'given', 'surname', 'and', 'address'] and
            last_name.lower() not in ['patient', 'name', 'first', 'last', 'given', 'surname', 'and', 'address']):
            return last_name
    
    # Fallback patterns
    patterns = [
        r"Name[:\s]*[A-Za-z]+\s+([A-Za-z]+)",  # Second word in "Name: John Doe"
        r"Last Name[:\s]*([A-Za-z]+)",
        r"Surname[:\s]*([A-Za-z]+)",
        r"Patient Last Name[:\s]*([A-Za-z]+)",
        r"Last[:\s]*([A-Za-z]+)",
        r"L\.?Name[:\s]*([A-Za-z]+)",
        r"Patient[:\s]*[A-Za-z]+\s+([A-Za-z]+)",  # Second word after "Patient:"
        r"[A-Z][a-z]+\s+([A-Z][a-z]+)",  # Second capitalized word (common name pattern)
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            # Filter out common non-name words
            if name.lower() not in ['patient', 'name', 'first', 'last', 'given', 'surname']:
                return name
    
    return None

def extract_date_of_birth(text: str) -> Optional[datetime]:
    """Extract date of birth from text using various patterns."""
    patterns = [
        r"Date of Birth[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        r"DOB[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        r"Birth Date[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        r"Born[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        r"Birth[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",  # Any date pattern
        r"(\d{4}-\d{2}-\d{2})",  # YYYY-MM-DD format
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            date_str = match.group(1)
            try:
                # Try different date formats
                for fmt in ["%m/%d/%Y", "%m/%d/%y", "%m-%d-%Y", "%m-%d-%y", "%Y-%m-%d"]:
                    try:
                        return datetime.strptime(date_str, fmt)
                    except ValueError:
                        continue
            except:
                continue
    
    return None 

def extract_text_with_ocr(pdf_content: bytes) -> Optional[str]:
    """
    Extract text from image-based PDF using OCR.
    """
    try:
        # Convert PDF pages to images
        print("🔄 Converting PDF pages to images...")
        images = convert_from_bytes(pdf_content, dpi=300)
        print(f"📷 Converted {len(images)} pages to images")
        
        # Extract text from each image using OCR
        all_text = ""
        for i, image in enumerate(images):
            print(f"🔍 Processing page {i+1} with OCR...")
            # Configure OCR for better accuracy
            custom_config = r'--oem 3 --psm 6'
            page_text = pytesseract.image_to_string(image, config=custom_config)
            all_text += page_text + "\n"
            print(f"   Page {i+1}: {len(page_text)} characters extracted")
        
        return all_text
        
    except Exception as e:
        print(f"❌ OCR Error: {str(e)}")
        return None 