from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import io
import requests
import easyocr
import logging
import time
import hashlib
import pdfplumber
from config import Config

router = APIRouter()

# Global OCR reader
reader = easyocr.Reader(['en'], gpu=False)  # Use CPU for stability

def extract_text_from_pdf(file_stream, reader):
    start_time = time.time()
    text = ""
    file_stream.seek(0)
    with pdfplumber.open(file_stream) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text += page_text
    if not text.strip():
        # No text extracted, try OCR on each page image
        text = ""
        file_stream.seek(0)
        with pdfplumber.open(file_stream) as pdf:
            for page_num, page in enumerate(pdf.pages):
                try:
                    pil_image = page.to_image(resolution=300).original
                    result = reader.readtext(pil_image)
                    page_text = " ".join([res[1] for res in result])
                    text += page_text + "\n"
                except Exception as e:
                    logging.error(f"Error during OCR processing of PDF page {page_num}: {str(e)}")
                    raise
    elapsed = time.time() - start_time
    logging.info(f"extract_text_from_pdf took {elapsed:.2f} seconds")
    return text

def extract_text_from_image(file_stream, reader):
    start_time = time.time()
    try:
        image = Image.open(file_stream)
        result = reader.readtext(image)
        text = " ".join([res[1] for res in result])
        elapsed = time.time() - start_time
        logging.info(f"extract_text_from_image took {elapsed:.2f} seconds")
        return text
    except Exception as e:
        logging.error(f"Error during OCR processing: {str(e)}")
        raise

def is_medical_report(text):
    medical_keywords = [
        "hemoglobin", "wbc", "rbc", "glucose", "platelets", "x-ray", "ct scan",
        "mri", "blood test", "cholesterol", "liver function", "kidney function",
        "diagnosis", "symptoms", "medications", "precautions", "patient", "disease",
        "treatment", "recommended", "summary", "allergy", "immune", "reaction",
        "treatment plan", "follow-up", "consultation", "prescription", "appointment"
    ]
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in medical_keywords)

def analyze_report(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={Config.GEMINI_API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [{
            "parts": [{
                "text": (
                    "You are a medical expert assistant. A user has uploaded their medical report. "
                    "Analyze the following report line-by-line in simple, easy-to-understand language. "
                    "Then suggest any recommended next steps if needed.\n\nMedical Report:\n"
                    f"{text}\n\nExplanation:"
                )
            }]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            response_json = response.json()
            if "candidates" in response_json and len(response_json["candidates"]) > 0:
                content = response_json["candidates"][0].get("content", "")
                if isinstance(content, dict) and "parts" in content:
                    text_parts = [part.get("text", "") for part in content["parts"] if isinstance(part, dict)]
                    return "".join(text_parts)
                else:
                    return content
            else:
                logging.error(f"Gemini API response missing candidates: {response_json}")
                return "Error: Unexpected Gemini API response format."
        else:
            logging.error(f"Gemini API error: {response.status_code} - {response.text}")
            return f"Error from Gemini API: {response.status_code} - {response.text}"
    except Exception as e:
        logging.error(f"Exception during Gemini API request: {str(e)}")
        return f"Exception during Gemini API request: {str(e)}"

@router.post('/analyze')
def analyze(file: UploadFile = File(...)):
    if not file.filename:
        logging.warning("Error: No selected file")
        raise HTTPException(status_code=400, detail="No selected file")

    try:
        # Compute SHA256 hash of file content for caching
        file_bytes = file.file.read()
        file_hash = hashlib.sha256(file_bytes).hexdigest()
        file.file.seek(0)

        # Check cache with TTL (1 hour)
        current_time = time.time()
        if file_hash in analyze.cache:
            cached_time, cached_result = analyze.cache[file_hash]
            if current_time - cached_time < 3600:  # 1 hour TTL
                logging.info(f"Cache hit for file hash {file_hash}")
                return cached_result
            else:
                del analyze.cache[file_hash]  # Expire old cache

        if file.content_type == "application/pdf":
            text = extract_text_from_pdf(file.file, reader)
        elif file.content_type in ["image/png", "image/jpeg", "image/jpg"]:
            text = extract_text_from_image(file.file, reader)
        else:
            logging.warning("Error: Unsupported file type")
            raise HTTPException(status_code=400, detail="Unsupported file type")

        if not text.strip():
            logging.warning("Error: No text could be extracted from the uploaded file.")
            raise HTTPException(status_code=400, detail="No text could be extracted from the uploaded file.")

        if not is_medical_report(text):
            logging.warning("Error: Invalid medical report uploaded")
            raise HTTPException(status_code=400, detail="This doesn't seem to be a valid medical report. Please upload a real medical report.")

        explanation = analyze_report(text)

        result = {
            "extracted_text": text,
            "explanation": explanation
        }

        # Cache the result with timestamp
        analyze.cache[file_hash] = (current_time, result)

        return result

    except Exception as e:
        warning_msg = f"WARNING:root:Error: {str(e)}"
        logging.error(warning_msg)
        raise HTTPException(status_code=500, detail=warning_msg)

# Initialize cache dictionary as a function attribute
analyze.cache = {}
