from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.user_model import User
from utils.auth import admin_login_required

admin_user_bp = Blueprint('admin_user_bp', __name__, url_prefix='/admin/users')

@admin_user_bp.route('/', methods=['GET'])
@admin_login_required
def list_users():
    try:
        db: Session = SessionLocal()
        users = db.query(User).all()
        db.close()
        users_data = []
        for user in users:
            users_data.append({
                'user_id': user.user_id,
                'name': user.name,
                'email': user.email,
                'age': user.age,
                'gender': user.gender,
                'is_active': user.is_active,
                'is_admin': user.is_admin
            })
        return jsonify(users_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_user_bp.route('/activate/<int:user_id>', methods=['POST'])
@admin_login_required
def activate_user(user_id):
    try:
        db: Session = SessionLocal()
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            db.close()
            return jsonify({'error': 'User not found'}), 404
        user.is_active = True
        db.commit()
        db.close()
        return jsonify({'message': 'User activated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_user_bp.route('/deactivate/<int:user_id>', methods=['POST'])
@admin_login_required
def deactivate_user(user_id):
    try:
        db: Session = SessionLocal()
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            db.close()
            return jsonify({'error': 'User not found'}), 404
        user.is_active = False
        db.commit()
        db.close()
        return jsonify({'message': 'User deactivated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_user_bp.route('/delete/<int:user_id>', methods=['DELETE'])
@admin_login_required
def delete_user(user_id):
    try:
        db: Session = SessionLocal()
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            db.close()
            return jsonify({'error': 'User not found'}), 404
        # Soft delete: set is_active to False and mark deleted flag if exists
        user.is_active = False
        user.is_deleted = True if hasattr(user, 'is_deleted') else False
        db.commit()
        db.close()
        return jsonify({'message': 'User deleted (soft) successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
