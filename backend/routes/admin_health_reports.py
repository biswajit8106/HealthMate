from flask import Blueprint, request, jsonify, send_file
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.health_report_model import HealthReport
from utils.auth import admin_login_required
import os

admin_health_reports_bp = Blueprint('admin_health_reports_bp', __name__, url_prefix='/admin/health_reports')

@admin_health_reports_bp.route('/', methods=['GET'])
@admin_login_required
def list_reports():
    try:
        db: Session = SessionLocal()
        query = db.query(HealthReport)

        user_id = request.args.get('user_id')
        disease = request.args.get('disease')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if user_id:
            query = query.filter(HealthReport.user_id == int(user_id))
        if disease:
            query = query.filter(HealthReport.predicted_disease.ilike(f"%{disease}%"))
        if start_date:
            query = query.filter(HealthReport.created_at >= start_date)
        if end_date:
            query = query.filter(HealthReport.created_at <= end_date)

        reports = query.all()
        db.close()

        reports_data = []
        for report in reports:
            reports_data.append({
                'id': report.id,
                'user_id': report.user_id,
                'name': report.name,
                'gender': report.gender,
                'age': report.age,
                'predicted_disease': report.predicted_disease,
                'confidence': report.confidence,
                'description': report.description,
                'created_at': report.created_at.isoformat()
            })
        return jsonify(reports_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_health_reports_bp.route('/download/<int:report_id>', methods=['GET'])
@admin_login_required
def download_report(report_id):
    try:
        # Assuming reports are saved as PDFs in a directory with filename pattern report_<id>.pdf
        report_path = f'backend/static/reports/report_{report_id}.pdf'
        if not os.path.exists(report_path):
            return jsonify({'error': 'Report file not found'}), 404
        return send_file(report_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_health_reports_bp.route('/delete/<int:report_id>', methods=['DELETE'])
@admin_login_required
def delete_report(report_id):
    try:
        db: Session = SessionLocal()
        report = db.query(HealthReport).filter(HealthReport.id == report_id).first()
        if not report:
            db.close()
            return jsonify({'error': 'Report not found'}), 404
        # Soft delete or archive logic can be implemented here
        db.delete(report)
        db.commit()
        db.close()
        return jsonify({'message': 'Report deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
