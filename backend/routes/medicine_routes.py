from flask import Blueprint, request, jsonify
from flask import Blueprint, request, jsonify, session
from sqlalchemy.orm import Session
import json, traceback
from database.db import SessionLocal
from models.health_report_model import HealthReport
from utils.auth import login_required
from utils.disease_medication_utils import disease_medication_data

medicine_bp = Blueprint('medicine', __name__)

@medicine_bp.route('/recent', methods=['GET'])
@login_required
def get_recent_medicine():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not logged in'}), 401

        db: Session = SessionLocal()
        recent_report = db.query(HealthReport).filter_by(user_id=user_id).order_by(HealthReport.created_at.desc()).first()
        db.close()

        if not recent_report:
            return jsonify({'message': 'No recent report found', 'predicted_disease': None, 'medications': []}), 200

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

        return jsonify({
            'predicted_disease': recent_report.predicted_disease,
            'medications': enriched_meds
        }), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
