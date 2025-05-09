from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from database.db import SessionLocal
from utils.auth import admin_login_required

admin_feedback_bp = Blueprint('admin_feedback_bp', __name__, url_prefix='/admin/feedback')

# For demonstration, using in-memory store. In production, use persistent storage.
feedback_store = []

@admin_feedback_bp.route('/', methods=['GET'])
@admin_login_required
def list_feedback():
    try:
        db: Session = SessionLocal()
        # For now, return all feedback from in-memory store
        return jsonify(feedback_store), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_feedback_bp.route('/reply/<int:feedback_id>', methods=['POST'])
@admin_login_required
def reply_feedback(feedback_id):
    try:
        data = request.json
        reply = data.get('reply')
        if not reply:
            return jsonify({'error': 'Reply content required'}), 400
        # Find feedback and add reply
        for fb in feedback_store:
            if fb.get('id') == feedback_id:
                fb['reply'] = reply
                fb['resolved'] = True
                return jsonify({'message': 'Reply added and feedback marked resolved'}), 200
        return jsonify({'error': 'Feedback not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_feedback_bp.route('/mark_resolved/<int:feedback_id>', methods=['POST'])
@admin_login_required
def mark_resolved(feedback_id):
    try:
        for fb in feedback_store:
            if fb.get('id') == feedback_id:
                fb['resolved'] = True
                return jsonify({'message': 'Feedback marked resolved'}), 200
        return jsonify({'error': 'Feedback not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
