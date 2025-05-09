from flask import Blueprint, request, jsonify, send_file
from sqlalchemy.orm import Session
from database.db import SessionLocal
from utils.auth import admin_login_required
import os

admin_analyzer_reports_bp = Blueprint('admin_analyzer_reports_bp', __name__, url_prefix='/admin/analyzer_reports')

# Assuming there is a model or database table for analyzer uploads, here we simulate with file system

UPLOAD_FOLDER = 'backend/static/analyzer_uploads'

@admin_analyzer_reports_bp.route('/', methods=['GET'])
@admin_login_required
def list_uploads():
    try:
        files = os.listdir(UPLOAD_FOLDER)
        uploads = []
        for filename in files:
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                uploads.append({
                    'filename': filename,
                    'size': os.path.getsize(filepath),
                    'path': filepath
                })
        return jsonify(uploads), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_analyzer_reports_bp.route('/download/<filename>', methods=['GET'])
@admin_login_required
def download_upload(filename):
    try:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_analyzer_reports_bp.route('/delete/<filename>', methods=['DELETE'])
@admin_login_required
def delete_upload(filename):
    try:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        os.remove(filepath)
        return jsonify({'message': 'File deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
