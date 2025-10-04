from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json, traceback
from database.db import get_db
from models.health_report_model import HealthReport
from utils.auth import get_current_user
from utils.disease_medication_utils import disease_medication_data

router = APIRouter()

@router.get('/recent')
def get_recent_medicine(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        recent_report = db.query(HealthReport).filter_by(user_id=user_id).order_by(HealthReport.created_at.desc()).first()

        if not recent_report:
            return {'message': 'No recent report found', 'predicted_disease': None, 'medications': []}

        medications = []
        try:
            medications = json.loads(recent_report.medications)
        except Exception:
            medications = []

        # Enrich medications with dosage and timing from CSV data
        enriched_meds = []
        disease = recent_report.predicted_disease.lower().strip() if recent_report.predicted_disease else ''
        for med in medications:
            med_name = med if isinstance(med, str) else med.get('name', '')
            med_lower = med_name.lower().strip()
            key = (disease, med_lower)
            dosage = ''
            timing = ''
            print(f"Looking up key: {key}")  # Debug print
            if key in disease_medication_data:
                dosage = disease_medication_data[key].get('dosage', '')
                timing = disease_medication_data[key].get('timing', '')
            else:
                print(f"Key not found in CSV data: {key}")  # Debug print
            enriched_meds.append({
                'name': med_name,
                'dosage': dosage,
                'timing': timing
            })

        return {
            'predicted_disease': recent_report.predicted_disease,
            'medications': enriched_meds
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
