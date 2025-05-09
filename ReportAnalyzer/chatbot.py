import streamlit as st
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import requests

# GROQ API key
GROQ_API_KEY = "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"

def extract_text_from_pdf(file):
    text = ""
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return text

def extract_text_from_image(file):
    image = Image.open(file)
    text = pytesseract.image_to_string(image)
    
    return text

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
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    prompt = (
        "You are a medical expert assistant. A user has uploaded their medical report. "
        "Analyze the following report line-by-line in simple, easy-to-understand language. "
        "Then suggest any recommended next steps if needed.\n\n"
        f"Medical Report:\n{text}\n\n"
        "Explanation:"
    )

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1500
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error from Groq API: {response.status_code} - {response.text}"

# Streamlit UI
st.title("🩺 Medical Report Analyzer Chatbot (Groq-powered)")

uploaded_file = st.file_uploader("📄 Upload your medical report (PDF/Image)", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        report_text = extract_text_from_pdf(uploaded_file)
    else:
        report_text = extract_text_from_image(uploaded_file)

    if report_text:
        if is_medical_report(report_text):
            st.subheader("📋 Extracted Text")
            st.text_area("", report_text, height=300)

            with st.spinner("Analyzing your report with Groq's LLaMA 3 model..."):
                explanation = analyze_report(report_text)

            st.subheader("🧠 Chatbot Explanation")
            st.write(explanation)
        else:
            st.error("⚠️ This doesn't seem to be a valid medical report. Please upload a real medical report.")
    else:
        st.warning("⚠️ No text could be extracted from the uploaded file.")
