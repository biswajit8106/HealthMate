import os
from flask import Blueprint, request, send_file, jsonify, session
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from sqlalchemy.orm import Session
import io, json, datetime, traceback, ast
from database.db import SessionLocal
from models.health_report_model import HealthReport
from models.user_model import User

import collections
from flask import Blueprint, request, send_file, jsonify, session
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from sqlalchemy.orm import Session
import io, json, datetime, traceback, ast
from database.db import SessionLocal
from models.health_report_model import HealthReport
from models.user_model import User

report_bp = Blueprint('report_bp', __name__)

# ----------------------------------------
# 1. Save and Generate PDF Report
# ----------------------------------------
from utils.auth import login_required

@report_bp.route('/save', methods=['POST'])
@login_required
def save_and_generate_report():
    try:
        data = request.get_json()
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not logged in'}), 401

        db: Session = SessionLocal()

        # Clean and process fields
        def clean_list(field):
            raw = data.get(field, [])
            if raw and isinstance(raw[0], str) and raw[0].startswith("["):
                return json.dumps(ast.literal_eval(raw[0]))
            return json.dumps(raw)

        report = HealthReport(
            user_id=user_id,
            name=data.get('name'),
            gender=data.get('gender'),
            age=data.get('age'),
            symptoms=json.dumps(data.get('symptoms', [])),
            predicted_disease=data.get('predicted_disease'),
            confidence=data.get('confidence'),
            description=data.get('description') or "No description available.",
            precautions=json.dumps(data.get('precautions', [])),
            medications=clean_list('medications'),
            diets=clean_list('diets'),
            workouts=json.dumps(data.get('workouts', [])),
            created_at=datetime.datetime.utcnow()
        )

        db.add(report)
        db.commit()
        db.refresh(report)
        db.close()

        # Generate PDF
        return generate_pdf_response(report)

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# ----------------------------------------
# 2. Get User Report History
# ----------------------------------------
@report_bp.route('/health/reports', methods=['GET'])
def get_user_health_reports():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not logged in'}), 401

        db: Session = SessionLocal()
        reports = db.query(HealthReport).filter_by(user_id=user_id).order_by(HealthReport.created_at.desc()).all()
        db.close()

        # Deduplicate reports by predicted_disease and created_at
        unique_reports = {}
        for r in reports:
            key = (r.predicted_disease, r.created_at)
            if key not in unique_reports:
                unique_reports[key] = r

        return jsonify([{
            'id': r.id,
            'title': f"{r.predicted_disease} Report",
            'name': r.name,
            'age': r.age,
            'gender': r.gender,
            'predicted_disease': r.predicted_disease,
            'confidence': r.confidence,
            'description': r.description,
            'date': r.created_at.isoformat() if r.created_at else None
        } for r in unique_reports.values()]), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# ----------------------------------------
# 3. Download Report by ID
# ----------------------------------------
@report_bp.route('/download/<int:report_id>', methods=['GET'])
def download_report(report_id):
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not logged in'}), 401

        db: Session = SessionLocal()
        report = db.query(HealthReport).filter_by(id=report_id, user_id=user_id).first()
        db.close()

        if not report:
            return jsonify({'error': 'Report not found'}), 404

        return generate_pdf_response(report)

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# ----------------------------------------
# 4. PDF Generator Helper
# ----------------------------------------
def generate_pdf_response(report):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    logo_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'logo.png')
    stamp_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'stamp.png')

    # Header
    c.drawImage(logo_path, 40, 780, width=100, height=40)
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(300, 770, " HealthMate Diagnostic Report")
    c.setFont("Helvetica-Oblique", 11)
    c.setFillColor(colors.grey)
    now = datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")
    c.drawCentredString(300, 750, f" Generated on: {now}")
    c.setFillColor(colors.black)

    y = 720
    gap = 22

    def draw_section(title, items):
        nonlocal y
        if y < 120:
            c.showPage()
            y = 780
        c.setFont("Helvetica-Bold", 13)
        c.setFillColor(colors.darkblue)
        c.drawString(40, y, title)
        y -= 16
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.black)

        if isinstance(items, list):
            for item in items:
                if y < 80:
                    c.showPage()
                    y = 780
                c.drawString(60, y, f"• {item}")
                y -= gap
        else:
            for line in str(items).split('\\n'):
                if y < 80:
                    c.showPage()
                    y = 780
                c.drawString(60, y, line)
                y -= gap
        y -= 8

    draw_section(" Patient Information", [
        f"Name: {report.name}",
        f"Gender: {report.gender}",
        f"Age: {report.age}"
    ])
    draw_section(" Diagnosis Summary", [
        f"Predicted Disease: {report.predicted_disease}",
        f"Confidence: {(float(report.confidence) * 100):.2f}%" if report.confidence else "N/A"
    ])
    draw_section(" Disease Description", report.description)
    draw_section(" Symptoms", json.loads(report.symptoms))
    draw_section(" Precautions", json.loads(report.precautions))
    draw_section(" Medications", json.loads(report.medications))
    draw_section(" Recommended Diets", json.loads(report.diets))
    draw_section(" Workouts & Activities", json.loads(report.workouts))

    c.drawImage(stamp_path, 430, 40, width=100, height=60)
    c.showPage()
    c.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{report.name}_health_report.pdf",
        mimetype='application/pdf'
    )
