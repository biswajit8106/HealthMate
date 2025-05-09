import json
import datetime
from flask import Blueprint, jsonify, session
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.db import SessionLocal
from models.health_report_model import HealthReport
from utils.auth import login_required

dashboard_charts_bp = Blueprint('dashboard_charts_bp', __name__, url_prefix='/report/dashboard')

@dashboard_charts_bp.route('/disease_categories', methods=['GET'])
@login_required
def get_disease_categories():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not logged in'}), 401

        db: Session = SessionLocal()
        # Aggregate count of predicted_disease for the user
        results = db.query(
            HealthReport.predicted_disease,
            func.count(HealthReport.predicted_disease)
        ).filter(
            HealthReport.user_id == user_id
        ).group_by(
            HealthReport.predicted_disease
        ).all()
        db.close()

        data = [{'disease': r[0], 'count': r[1]} for r in results]
        return jsonify(data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_charts_bp.route('/health_trends', methods=['GET'])
@login_required
def get_health_trends():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not logged in'}), 401

        db: Session = SessionLocal()
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
        db.close()

        data = [{'date': r[0].isoformat(), 'count': r[1]} for r in results]
        return jsonify(data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_charts_bp.route('/common_symptoms', methods=['GET'])
@login_required
def get_common_symptoms():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not logged in'}), 401

        db: Session = SessionLocal()
        reports = db.query(HealthReport.symptoms).filter(HealthReport.user_id == user_id).all()
        db.close()

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
        return jsonify(data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_charts_bp.route('/symptom_disease_heatmap', methods=['GET'])
@login_required
def get_symptom_disease_heatmap():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not logged in'}), 401

        db: Session = SessionLocal()
        reports = db.query(HealthReport.symptoms, HealthReport.predicted_disease).filter(HealthReport.user_id == user_id).all()
        db.close()

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

        return jsonify(data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
