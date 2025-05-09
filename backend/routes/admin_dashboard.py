import logging

from flask import Blueprint, jsonify
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from database.db import SessionLocal
from models.user_model import User
from models.health_report_model import HealthReport
from utils.auth import admin_login_required
import os
import datetime

logger = logging.getLogger(__name__)

admin_dashboard_bp = Blueprint('admin_dashboard_bp', __name__, url_prefix='/admin/dashboard')

@admin_dashboard_bp.route('/stats', methods=['GET'])
@admin_login_required
def get_stats():
    db: Session = None
    try:
        db = SessionLocal()
        total_users = db.query(func.count(User.user_id)).scalar()
        total_reports = db.query(func.count(HealthReport.id)).scalar()
        analyzer_uploads_folder = 'backend/static/analyzer_uploads'
        total_analyzer_uploads = 0
        if os.path.exists(analyzer_uploads_folder) and os.path.isdir(analyzer_uploads_folder):
            total_analyzer_uploads = len([f for f in os.listdir(analyzer_uploads_folder) if os.path.isfile(os.path.join(analyzer_uploads_folder, f))])
        return jsonify({
            'total_users': total_users,
            'total_reports': total_reports,
            'total_analyzer_uploads': total_analyzer_uploads
        }), 200
    except Exception as e:
        logger.exception("Error in get_stats")
        return jsonify({'error': str(e)}), 500
    finally:
        if db:
            db.close()

@admin_dashboard_bp.route('/user_growth', methods=['GET'])
@admin_login_required
def user_growth():
    db: Session = None
    try:
        db = SessionLocal()
        results = db.query(
            extract('year', User.created_at).label('year'),
            extract('month', User.created_at).label('month'),
            func.count(User.user_id)
        ).group_by('year', 'month').order_by('year', 'month').all()
        data = [{'year': r[0], 'month': r[1], 'count': r[2]} for r in results]
        return jsonify(data), 200
    except Exception as e:
        logger.exception("Error in user_growth")
        return jsonify({'error': str(e)}), 500
    finally:
        if db:
            db.close()

@admin_dashboard_bp.route('/symptom_check_usage', methods=['GET'])
@admin_login_required
def symptom_check_usage():
    db: Session = None
    try:
        db = SessionLocal()
        results = db.query(
            func.date(HealthReport.created_at),
            func.count(HealthReport.id)
        ).group_by(func.date(HealthReport.created_at)).order_by(func.date(HealthReport.created_at)).all()
        data = [{'date': r[0].isoformat(), 'count': r[1]} for r in results]
        return jsonify(data), 200
    except Exception as e:
        logger.exception("Error in symptom_check_usage")
        return jsonify({'error': str(e)}), 500
    finally:
        if db:
            db.close()

@admin_dashboard_bp.route('/report_analyzer_trends', methods=['GET'])
@admin_login_required
def report_analyzer_trends():
    try:
        analyzer_uploads_folder = 'backend/static/analyzer_uploads'
        date_counts = {}
        if os.path.exists(analyzer_uploads_folder) and os.path.isdir(analyzer_uploads_folder):
            files = os.listdir(analyzer_uploads_folder)
            for f in files:
                path = os.path.join(analyzer_uploads_folder, f)
                if os.path.isfile(path):
                    mod_time = os.path.getmtime(path)
                    date_str = datetime.datetime.fromtimestamp(mod_time).date().isoformat()
                    date_counts[date_str] = date_counts.get(date_str, 0) + 1
        data = [{'date': k, 'count': v} for k, v in sorted(date_counts.items())]
        return jsonify(data), 200
    except Exception as e:
        logger.exception("Error in report_analyzer_trends")
        return jsonify({'error': str(e)}), 500

@admin_dashboard_bp.route('/recent_activity', methods=['GET'])
@admin_login_required
def recent_activity():
    db: Session = None
    try:
        db = SessionLocal()
        recent_users = db.query(User).order_by(User.created_at.desc()).limit(10).all()
        recent_reports = db.query(HealthReport).order_by(HealthReport.created_at.desc()).limit(10).all()
        users_data = [{
            'type': 'user_registration',
            'user_id': u.user_id,
            'name': u.name,
            'created_at': u.created_at.isoformat() if u.created_at else None
        } for u in recent_users]
        reports_data = [{
            'type': 'report_generated',
            'report_id': r.id,
            'user_id': r.user_id,
            'predicted_disease': r.predicted_disease,
            'created_at': r.created_at.isoformat() if r.created_at else None
        } for r in recent_reports]
        combined = users_data + reports_data
        combined_sorted = sorted(combined, key=lambda x: x['created_at'] or '', reverse=True)
        return jsonify(combined_sorted[:10]), 200
    except Exception as e:
        logger.exception("Error in recent_activity")
        return jsonify({'error': str(e)}), 500
    finally:
        if db:
            db.close()
