from flask import Blueprint, request, jsonify, session
from database.db import get_db
from models.health_report_model import HealthReport
from sqlalchemy.orm import Session
import json
from utils.auth import login_required

medical_history_bp = Blueprint('medical_history_bp', __name__, url_prefix='/api/user/medical_history')

import logging

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

@medical_history_bp.route('', methods=['GET'], strict_slashes=False)
@medical_history_bp.route('/', methods=['GET'], strict_slashes=False)
@login_required
def get_medical_history():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401

        db: Session = next(get_db())
        reports = db.query(HealthReport).filter_by(user_id=user_id).all()

        if not reports:
            return jsonify({'error': 'Medical history not found'}), 404

        # Deduplicate reports by predicted_disease and created_at
        unique_reports = {}
        for r in reports:
            key = (r.predicted_disease, r.created_at)
            if key not in unique_reports:
                unique_reports[key] = r

        return jsonify([serialize_report(r) for r in unique_reports.values()]), 200

    except Exception as e:
        logging.error(f"Error in get_medical_history: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

@medical_history_bp.route('/<int:report_id>', methods=['GET'])
@login_required
def get_medical_history_by_id(report_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    db: Session = next(get_db())
    report = db.query(HealthReport).filter_by(id=report_id, user_id=user_id).first()

    if not report:
        return jsonify({'error': 'Medical history not found'}), 404

    return jsonify(serialize_report(report)), 200

@medical_history_bp.route('/list', methods=['GET'])
@login_required
def list_medical_history_reports():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    db: Session = next(get_db())
    reports = db.query(HealthReport).filter_by(user_id=user_id).all()
    report_list = [{'id': r.id, 'name': r.name} for r in reports]
    return jsonify(report_list), 200

@medical_history_bp.route('', methods=['PUT'], strict_slashes=False)
@medical_history_bp.route('/', methods=['PUT'], strict_slashes=False)
@login_required
def update_medical_history():
    data = request.get_json()
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    report_id = data.get('id')

    if not report_id:
        return jsonify({'error': 'Missing id'}), 400

    db: Session = next(get_db())
    report = db.query(HealthReport).filter_by(id=report_id, user_id=user_id).first()

    if not report:
        return jsonify({'error': 'Medical history not found'}), 404

    # Update fields if provided
    report.name = data.get('name', report.name)
    report.gender = data.get('gender', report.gender)
    report.age = data.get('age', report.age)
    report.symptoms = json.dumps(data.get('symptoms', json.loads(report.symptoms) if report.symptoms else []))
    report.predicted_disease = data.get('predicted_disease', report.predicted_disease)
    report.confidence = data.get('confidence', report.confidence)
    report.description = data.get('description', report.description)
    report.precautions = json.dumps(data.get('precautions', json.loads(report.precautions) if report.precautions else []))
    report.medications = json.dumps(data.get('medications', json.loads(report.medications) if report.medications else []))
    report.diets = json.dumps(data.get('diets', json.loads(report.diets) if report.diets else []))
    report.workouts = json.dumps(data.get('workouts', json.loads(report.workouts) if report.workouts else []))

    try:
        db.commit()
        return jsonify({'message': 'Medical history updated successfully'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

@medical_history_bp.route('', methods=['POST'], strict_slashes=False)
@medical_history_bp.route('/', methods=['POST'], strict_slashes=False)
@login_required
def create_medical_history():
    data = request.get_json()
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    try:
        db: Session = next(get_db())
        new_report = HealthReport(
            user_id=user_id,
            name=data.get('name'),
            gender=data.get('gender'),
            age=data.get('age'),
            symptoms=json.dumps(data.get('symptoms', [])),
            predicted_disease=data.get('predicted_disease'),
            confidence=data.get('confidence'),
            description=data.get('description'),
            precautions=json.dumps(data.get('precautions', [])),
            medications=json.dumps(data.get('medications', [])),
            diets=json.dumps(data.get('diets', [])),
            workouts=json.dumps(data.get('workouts', []))
        )
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
        return jsonify({'message': 'Medical history created successfully', 'id': new_report.id}), 201
    except Exception as e:
        db.rollback()
        logging.error(f"Error in create_medical_history: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500
