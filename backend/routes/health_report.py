import os
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from sqlalchemy.orm import Session
import io, json, datetime, traceback, ast
from database.db import get_db
from models.health_report_model import HealthReport
from models.user_model import User
from utils.auth import get_current_user
from pydantic import BaseModel

router = APIRouter()

class SaveReportRequest(BaseModel):
    name: str
    gender: str
    age: int
    symptoms: list[str]
    predicted_disease: str
    confidence: float
    description: str = "No description available."
    precautions: list[str]
    medications: list[str]
    diets: list[str]
    workouts: list[str]

@router.post('/save')
def save_and_generate_report(request_data: SaveReportRequest, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        # Clean and process fields
        def clean_list(field):
            raw = getattr(request_data, field, [])
            if raw and isinstance(raw[0], str) and raw[0].startswith("["):
                return json.dumps(ast.literal_eval(raw[0]))
            return json.dumps(raw)

        report = HealthReport(
            user_id=user_id,
            name=request_data.name,
            gender=request_data.gender,
            age=request_data.age,
            symptoms=json.dumps(request_data.symptoms),
            predicted_disease=request_data.predicted_disease,
            confidence=request_data.confidence,
            description=request_data.description,
            precautions=json.dumps(request_data.precautions),
            medications=clean_list('medications'),
            diets=clean_list('diets'),
            workouts=json.dumps(request_data.workouts),
            created_at=datetime.datetime.utcnow()
        )

        db.add(report)
        db.commit()
        db.refresh(report)

        # Generate PDF
        buffer = generate_pdf_buffer(report)
        return StreamingResponse(
            buffer,
            media_type='application/pdf',
            headers={"Content-Disposition": f"attachment; filename={report.name}_health_report.pdf"}
        )

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------------------
# 2. Get User Report History
# ----------------------------------------
@router.get('/health/reports')
def get_user_health_reports(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        reports = db.query(HealthReport).filter_by(user_id=user_id).order_by(HealthReport.created_at.desc()).all()

        # Deduplicate reports by predicted_disease and created_at
        unique_reports = {}
        for r in reports:
            key = (r.predicted_disease, r.created_at)
            if key not in unique_reports:
                unique_reports[key] = r

        return [{
            'id': r.id,
            'title': f"{r.predicted_disease} Report",
            'name': r.name,
            'age': r.age,
            'gender': r.gender,
            'predicted_disease': r.predicted_disease,
            'confidence': r.confidence,
            'description': r.description,
            'date': r.created_at.isoformat() if r.created_at else None
        } for r in unique_reports.values()]

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------------------
# 3. Download Report by ID
# ----------------------------------------
@router.get('/download/{report_id}')
def download_report(report_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        report = db.query(HealthReport).filter_by(id=report_id, user_id=user_id).first()

        if not report:
            raise HTTPException(status_code=404, detail='Report not found')

        buffer = generate_pdf_buffer(report)
        return StreamingResponse(
            buffer,
            media_type='application/pdf',
            headers={"Content-Disposition": f"attachment; filename={report.name}_health_report.pdf"}
        )

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------------------
# 4. PDF Generator Helper
# ----------------------------------------
def generate_pdf_buffer(report):
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

    return buffer
