from flask import Blueprint, request, jsonify
import fitz  # PyMuPDF
from PIL import Image
import io
import requests
import easyocr
import logging
import time
import hashlib

reportanalyzer_bp = Blueprint('reportanalyzer_bp', __name__)

# GROQ API key
GEMINI_API_KEY = "AIzaSyBxBG3r8vYoLWcKP63Z9RniJeTNHyMbdE8"

# Enable GPU for easyocr if available
try:
    reader = easyocr.Reader(['en'], gpu=True)
    logging.info("easyocr initialized with GPU support.")
except Exception as e:
    logging.warning(f"easyocr GPU initialization failed, falling back to CPU. Error: {str(e)}")
    reader = easyocr.Reader(['en'], gpu=False)

def extract_text_from_pdf(file_stream):
    start_time = time.time()
    text = ""
    file_stream.seek(0)
    pdf = fitz.open(stream=file_stream.read(), filetype="pdf")
    for page in pdf:
        page_text = page.get_text()
        text += page_text
    if not text.strip():
        # No text extracted, try OCR on each page image
        text = ""
        for page_num in range(len(pdf)):
            page = pdf.load_page(page_num)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            try:
                result = reader.readtext(img)
                page_text = " ".join([res[1] for res in result])
                text += page_text + "\n"
            except Exception as e:
                logging.error(f"Error during OCR processing of PDF page {page_num}: {str(e)}")
                raise
    elapsed = time.time() - start_time
    logging.info(f"extract_text_from_pdf took {elapsed:.2f} seconds")
    return text

def extract_text_from_image(file_stream):
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
    import logging
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [{
            "parts": [{"text": f"You are a medical expert assistant. A user has uploaded their medical report. Analyze the following report line-by-line in simple, easy-to-understand language. Then suggest any recommended next steps if needed.\n\nMedical Report:\n{text}\n\nExplanation:"}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            response_json = response.json()
            # Extract generated content from Gemini API response
            if "candidates" in response_json and len(response_json["candidates"]) > 0:
                content = response_json["candidates"][0].get("content", "")
                # If content is a dict with parts, concatenate text parts
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

@reportanalyzer_bp.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Compute SHA256 hash of file content for caching
        file.seek(0)
        file_bytes = file.read()
        file_hash = hashlib.sha256(file_bytes).hexdigest()
        file.seek(0)

        # Check cache
        if file_hash in analyze.cache:
            logging.info(f"Cache hit for file hash {file_hash}")
            cached_result = analyze.cache[file_hash]
            return jsonify(cached_result)

        if file.content_type == "application/pdf":
            text = extract_text_from_pdf(file)
        elif file.content_type in ["image/png", "image/jpeg", "image/jpg"]:
            text = extract_text_from_image(file)
        else:
            return jsonify({"error": "Unsupported file type"}), 400

        if not text.strip():
            return jsonify({"error": "No text could be extracted from the uploaded file."}), 400

        if not is_medical_report(text):
            return jsonify({"error": "This doesn't seem to be a valid medical report. Please upload a real medical report."}), 400

        explanation = analyze_report(text)

        result = {
            "extracted_text": text,
            "explanation": explanation
        }

        # Cache the result
        analyze.cache[file_hash] = result

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"An error occurred during processing: {str(e)}"}), 500

# Initialize cache dictionary as a function attribute
analyze.cache = {}
