import csv
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from utils.auth import get_current_admin
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# In-memory store for symptoms to disease mapping override
symptom_disease_map = {}

class DiseaseRequest(BaseModel):
    name: str
    description: Optional[str] = ""
    medications: Optional[list] = []
    diets: Optional[list] = []
    workouts: Optional[list] = []
    precautions: Optional[list] = []

class SymptomMapRequest(BaseModel):
    symptom: str
    disease: str

@router.get('/')
def list_diseases(admin_id: int = Depends(get_current_admin)):
    try:
        # Use absolute path based on project root for CSV file
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        csv_file_path = os.path.join(base_dir, 'backend', 'Training', 'MasterData', 'disease_medication_details_with_timings.csv')
        if not os.path.exists(csv_file_path):
            raise HTTPException(status_code=500, detail=f'CSV file not found at {csv_file_path}')
        diseases = {}
        with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, skipinitialspace=True)
            for row in reader:
                disease = row.get('Disease', '').strip()
                if not disease:
                    continue
                if disease not in diseases:
                    diseases[disease] = {
                        'name': disease,
                        'description': '',
                        'medications': [],
                        'diets': [],
                        'workouts': [],
                        'precautions': []
                    }
                med = row.get('Medicine Name', '').strip()
                if med and med not in diseases[disease]['medications']:
                    diseases[disease]['medications'].append(med)
        return list(diseases.values())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/')
def add_disease(request_data: DiseaseRequest, admin_id: int = Depends(get_current_admin)):
    try:
        # Here, implement logic to add disease data to persistent storage or CSV
        # For now, just return success
        return {'message': 'Disease added successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put('/{disease_name}')
def update_disease(disease_name: str, request_data: DiseaseRequest, admin_id: int = Depends(get_current_admin)):
    try:
        # Implement update logic here
        return {'message': f'Disease {disease_name} updated successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete('/{disease_name}')
def delete_disease(disease_name: str, admin_id: int = Depends(get_current_admin)):
    try:
        # Implement delete logic here
        return {'message': f'Disease {disease_name} deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/bulk_upload')
def bulk_upload(file: UploadFile = File(...), admin_id: int = Depends(get_current_admin)):
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail='No selected file')
        # Save and process CSV file for bulk upload
        # For now, just return success
        return {'message': 'Bulk upload successful'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/map_symptom')
def map_symptom(request_data: SymptomMapRequest, admin_id: int = Depends(get_current_admin)):
    try:
        if not request_data.symptom or not request_data.disease:
            raise HTTPException(status_code=400, detail='Symptom and disease required')
        symptom_disease_map[request_data.symptom.lower()] = request_data.disease
        return {'message': f'Symptom {request_data.symptom} mapped to disease {request_data.disease}'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
