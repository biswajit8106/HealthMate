from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from database.db import SessionLocal
from utils.auth import admin_login_required
import csv
import os

admin_disease_info_bp = Blueprint('admin_disease_info_bp', __name__, url_prefix='/admin/disease_info')

# In-memory store for symptoms to disease mapping override
symptom_disease_map = {}

import traceback
import logging

@admin_disease_info_bp.route('/', methods=['GET'])
@admin_login_required
def list_diseases():
    try:
        # Use absolute path based on project root for CSV file
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        csv_file_path = os.path.join(base_dir, 'backend', 'Training', 'MasterData', 'disease_medication_details_with_timings.csv')
        if not os.path.exists(csv_file_path):
            logging.error(f'CSV file not found at {csv_file_path}')
            return jsonify({'error': f'CSV file not found at {csv_file_path}'}), 500
        diseases = {}
        logging.debug(f'Opening CSV file at {csv_file_path}')
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
        logging.debug(f'Successfully read {len(diseases)} diseases from CSV')
        return jsonify(list(diseases.values())), 200
    except Exception as e:
        logging.error(f'Exception in list_diseases: {str(e)}')
        logging.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@admin_disease_info_bp.route('/', methods=['POST'])
@admin_login_required
def add_disease():
    try:
        data = request.json
        # Here, implement logic to add disease data to persistent storage or CSV
        # For now, just return success
        return jsonify({'message': 'Disease added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_disease_info_bp.route('/<disease_name>', methods=['PUT'])
@admin_login_required
def update_disease(disease_name):
    try:
        data = request.json
        # Implement update logic here
        return jsonify({'message': f'Disease {disease_name} updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_disease_info_bp.route('/<disease_name>', methods=['DELETE'])
@admin_login_required
def delete_disease(disease_name):
    try:
        # Implement delete logic here
        return jsonify({'message': f'Disease {disease_name} deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_disease_info_bp.route('/bulk_upload', methods=['POST'])
@admin_login_required
def bulk_upload():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        # Save and process CSV file for bulk upload
        # For now, just return success
        return jsonify({'message': 'Bulk upload successful'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_disease_info_bp.route('/map_symptom', methods=['POST'])
@admin_login_required
def map_symptom():
    try:
        data = request.json
        symptom = data.get('symptom')
        disease = data.get('disease')
        if not symptom or not disease:
            return jsonify({'error': 'Symptom and disease required'}), 400
        symptom_disease_map[symptom.lower()] = disease
        return jsonify({'message': f'Symptom {symptom} mapped to disease {disease}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
