from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models.health_report_model import HealthReport
from pydantic import BaseModel
from typing import List, Optional
import json
from utils.auth import get_current_user

router = APIRouter()

class MedicalHistoryBase(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    symptoms: Optional[List[str]] = []
    predicted_disease: Optional[str] = None
    confidence: Optional[float] = None
    description: Optional[str] = None
    precautions: Optional[List[str]] = []
    medications: Optional[List[str]] = []
    diets: Optional[List[str]] = []
    workouts: Optional[List[str]] = []

class MedicalHistoryCreate(MedicalHistoryBase):
    name: str
    gender: str
    age: int
    predicted_disease: str
    confidence: float

class MedicalHistoryUpdate(MedicalHistoryBase):
    id: int

class MedicalHistoryResponse(MedicalHistoryBase):
    id: int
    created_at: Optional[str] = None

    class Config:
        from_attributes = True

def serialize_report(report):
    return {
        'id': report.id,
        'name': report.name,
        'gender': report.gender,
        'age': report.age,
        'symptoms': json.loads(report.symptoms) if report.symptoms else [],
        'predicted_disease': report.predicted_disease,
        'confidence': report.confidence,
        'description': report.description,
        'precautions': json.loads(report.precautions) if report.precautions else [],
        'medications': json.loads(report.medications) if report.medications else [],
        'diets': json.loads(report.diets) if report.diets else [],
        'workouts': json.loads(report.workouts) if report.workouts else [],
        'created_at': report.created_at.isoformat() if report.created_at else None
    }

@router.get('', response_model=List[MedicalHistoryResponse])
def get_medical_history(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    reports = db.query(HealthReport).filter_by(user_id=user_id).all()

    if not reports:
        raise HTTPException(status_code=404, detail='Medical history not found')

    # Deduplicate reports by predicted_disease and created_at
    unique_reports = {}
    for r in reports:
        key = (r.predicted_disease, r.created_at)
        if key not in unique_reports:
            unique_reports[key] = r

    return [serialize_report(r) for r in unique_reports.values()]

@router.get('/{report_id}', response_model=MedicalHistoryResponse)
def get_medical_history_by_id(report_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    report = db.query(HealthReport).filter_by(id=report_id, user_id=user_id).first()

    if not report:
        raise HTTPException(status_code=404, detail='Medical history not found')

    return serialize_report(report)

@router.get('/list')
def list_medical_history_reports(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    reports = db.query(HealthReport).filter_by(user_id=user_id).all()
    report_list = [{'id': r.id, 'name': r.name} for r in reports]
    return report_list

@router.put('', response_model=dict)
def update_medical_history(request_data: MedicalHistoryUpdate, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    report = db.query(HealthReport).filter_by(id=request_data.id, user_id=user_id).first()

    if not report:
        raise HTTPException(status_code=404, detail='Medical history not found')

    # Update fields if provided
    if request_data.name is not None:
        report.name = request_data.name
    if request_data.gender is not None:
        report.gender = request_data.gender
    if request_data.age is not None:
        report.age = request_data.age
    if request_data.symptoms is not None:
        report.symptoms = json.dumps(request_data.symptoms)
    if request_data.predicted_disease is not None:
        report.predicted_disease = request_data.predicted_disease
    if request_data.confidence is not None:
        report.confidence = request_data.confidence
    if request_data.description is not None:
        report.description = request_data.description
    if request_data.precautions is not None:
        report.precautions = json.dumps(request_data.precautions)
    if request_data.medications is not None:
        report.medications = json.dumps(request_data.medications)
    if request_data.diets is not None:
        report.diets = json.dumps(request_data.diets)
    if request_data.workouts is not None:
        report.workouts = json.dumps(request_data.workouts)

    try:
        db.commit()
        return {'message': 'Medical history updated successfully'}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post('', response_model=dict)
def create_medical_history(request_data: MedicalHistoryCreate, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        new_report = HealthReport(
            user_id=user_id,
            name=request_data.name,
            gender=request_data.gender,
            age=request_data.age,
            symptoms=json.dumps(request_data.symptoms),
            predicted_disease=request_data.predicted_disease,
            confidence=request_data.confidence,
            description=request_data.description,
            precautions=json.dumps(request_data.precautions),
            medications=json.dumps(request_data.medications),
            diets=json.dumps(request_data.diets),
            workouts=json.dumps(request_data.workouts)
        )
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
        return {'message': 'Medical history created successfully', 'id': new_report.id}
    except Exception as e:
        db.rollback()
