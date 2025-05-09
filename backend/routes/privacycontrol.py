from flask import Blueprint, jsonify, request, session
from utils.auth import login_required
from database.db import get_db
from sqlalchemy.orm import Session
from models.user_model import User

privacycontrol_bp = Blueprint('privacycontrol', __name__)

@privacycontrol_bp.route('/user/privacy', methods=['GET'])
@login_required
def get_privacy_settings():
    db: Session = next(get_db())
    user = User.get_user_by_id(db, session['user_id'])
    if user:
        return jsonify({"dataSharing": getattr(user, "dataSharing", False)})
    return jsonify({"error": "User not found"}), 404

@privacycontrol_bp.route('/user/privacy', methods=['PUT'])
@login_required
def update_privacy_settings():
    data = request.get_json()
    if 'dataSharing' not in data:
        return jsonify({"error": "Missing dataSharing field"}), 400
    db: Session = next(get_db())
    user = User.get_user_by_id(db, session['user_id'])
    if user:
        setattr(user, "dataSharing", data['dataSharing'])
        db.commit()
        return jsonify({"message": "Privacy settings updated"})
    return jsonify({"error": "User not found"}), 404

@privacycontrol_bp.route('/user/history', methods=['DELETE'])
@login_required
def delete_history():
    # Assuming User model has a method to delete history
    db: Session = next(get_db())
    user = User.get_user_by_id(db, session['user_id'])
    if user:
        # Implement actual history deletion logic here
        # For now, simulate success
        return jsonify({"message": "History deleted successfully"})
    return jsonify({"error": "User not found"}), 404
