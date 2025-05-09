from flask import Blueprint, jsonify, request
from sqlalchemy.orm import Session
from database.db import SessionLocal
from utils.auth import admin_login_required
import datetime

admin_system_logs_bp = Blueprint('admin_system_logs_bp', __name__, url_prefix='/admin/system_logs')

# For demonstration, using in-memory logs. In production, use persistent storage.
activity_logs = []
failed_login_attempts = []
admin_login_ips = {}

@admin_system_logs_bp.route('/activity', methods=['GET'])
@admin_login_required
def get_activity_logs():
    try:
        # Return last 100 activity logs
        return jsonify(activity_logs[-100:]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_system_logs_bp.route('/failed_logins', methods=['GET'])
@admin_login_required
def get_failed_logins():
    try:
        # Return last 100 failed login attempts
        return jsonify(failed_login_attempts[-100:]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_system_logs_bp.route('/login_ip', methods=['POST'])
@admin_login_required
def record_login_ip():
    try:
        data = request.json
        admin_id = data.get('admin_id')
        ip = data.get('ip')
        if not admin_id or not ip:
            return jsonify({'error': 'admin_id and ip required'}), 400
        admin_login_ips.setdefault(admin_id, []).append({'ip': ip, 'timestamp': datetime.datetime.utcnow().isoformat()})
        return jsonify({'message': 'IP recorded'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_system_logs_bp.route('/session_management', methods=['GET'])
@admin_login_required
def get_sessions():
    try:
        # Placeholder for session management data
        sessions = [
            {'session_id': 'abc123', 'admin_id': 1, 'login_time': '2024-01-01T12:00:00Z', 'active': True},
            {'session_id': 'def456', 'admin_id': 2, 'login_time': '2024-01-02T08:30:00Z', 'active': False},
        ]
        return jsonify(sessions), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
