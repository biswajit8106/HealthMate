import json
import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.db import get_db
from models.health_report_model import HealthReport
from utils.auth import get_current_user

router = APIRouter()

@router.get('/disease_categories')
def get_disease_categories(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        # Aggregate count of predicted_disease for the user
        results = db.query(
            HealthReport.predicted_disease,
            func.count(HealthReport.predicted_disease)
        ).filter(
            HealthReport.user_id == user_id
        ).group_by(
            HealthReport.predicted_disease
        ).all()

        data = [{'disease': r[0], 'count': r[1]} for r in results]
        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/health_trends')
def get_health_trends(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        # Aggregate count of reports per date (day) for the user
        results = db.query(
            func.date(HealthReport.created_at),
            func.count(HealthReport.id)
        ).filter(
            HealthReport.user_id == user_id
        ).group_by(
            func.date(HealthReport.created_at)
        ).order_by(
            func.date(HealthReport.created_at)
        ).all()

        data = [{'date': r[0].isoformat(), 'count': r[1]} for r in results]
        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/common_symptoms')
def get_common_symptoms(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        reports = db.query(HealthReport.symptoms).filter(HealthReport.user_id == user_id).all()

        symptom_counts = {}
        for (symptoms_json,) in reports:
            symptoms = json.loads(symptoms_json) if symptoms_json else []
            for symptom in symptoms:
                symptom_counts[symptom] = symptom_counts.get(symptom, 0) + 1

        # Convert to list of dicts sorted by count descending
        data = sorted(
            [{'symptom': k, 'count': v} for k, v in symptom_counts.items()],
            key=lambda x: x['count'],
            reverse=True
        )
        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/symptom_disease_heatmap')
def get_symptom_disease_heatmap(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        reports = db.query(HealthReport.symptoms, HealthReport.predicted_disease).filter(HealthReport.user_id == user_id).all()

        heatmap_data = {}
        for symptoms_json, disease in reports:
            symptoms = json.loads(symptoms_json) if symptoms_json else []
            for symptom in symptoms:
                if symptom not in heatmap_data:
                    heatmap_data[symptom] = {}
                heatmap_data[symptom][disease] = heatmap_data[symptom].get(disease, 0) + 1

        # Convert to list of {symptom, disease, count} for frontend heatmap rendering
        data = []
        for symptom, diseases in heatmap_data.items():
            for disease, count in diseases.items():
                data.append({'symptom': symptom, 'disease': disease, 'count': count})

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
