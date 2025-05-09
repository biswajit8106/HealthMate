from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.user_model import User
from utils.auth import admin_login_required
from werkzeug.security import generate_password_hash

admin_user_controls_bp = Blueprint('admin_user_controls_bp', __name__, url_prefix='/admin/user_controls')

@admin_user_controls_bp.route('/admins', methods=['GET'])
@admin_login_required
def list_admins():
    try:
        db: Session = SessionLocal()
        admins = db.query(User).filter(User.is_admin == True).all()
        db.close()
        admins_data = []
        for admin in admins:
            admins_data.append({
                'user_id': admin.user_id,
                'name': admin.name,
                'email': admin.email,
                'role': admin.role if hasattr(admin, 'role') else 'Moderator',
            })
        return jsonify(admins_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_user_controls_bp.route('/admins', methods=['POST'])
@admin_login_required
def add_admin():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'Moderator')

        if not name or not email or not password:
            return jsonify({'error': 'Name, email and password are required'}), 400

        db: Session = SessionLocal()
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            db.close()
            return jsonify({'error': 'Admin with this email already exists'}), 400

        hashed_password = generate_password_hash(password)
        new_admin = User(name=name, email=email, password=hashed_password, is_admin=True, role=role)
        db.add(new_admin)
        db.commit()
        db.close()
        return jsonify({'message': 'Admin added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_user_controls_bp.route('/admins/<int:user_id>', methods=['DELETE'])
@admin_login_required
def remove_admin(user_id):
    try:
        db: Session = SessionLocal()
        admin = db.query(User).filter(User.user_id == user_id, User.is_admin == True).first()
        if not admin:
            db.close()
            return jsonify({'error': 'Admin not found'}), 404
        db.delete(admin)
        db.commit()
        db.close()
        return jsonify({'message': 'Admin removed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_user_controls_bp.route('/admins/<int:user_id>/role', methods=['PUT'])
@admin_login_required
def change_role(user_id):
    try:
        data = request.json
        new_role = data.get('role')
        if not new_role:
            return jsonify({'error': 'Role is required'}), 400
        db: Session = SessionLocal()
        admin = db.query(User).filter(User.user_id == user_id, User.is_admin == True).first()
        if not admin:
            db.close()
            return jsonify({'error': 'Admin not found'}), 404
        admin.role = new_role
        db.commit()
        db.close()
        return jsonify({'message': 'Role updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_user_controls_bp.route('/admins/<int:user_id>/password', methods=['PUT'])
@admin_login_required
def change_password(user_id):
    try:
        data = request.json
        new_password = data.get('password')
        if not new_password:
            return jsonify({'error': 'Password is required'}), 400
        db: Session = SessionLocal()
        admin = db.query(User).filter(User.user_id == user_id, User.is_admin == True).first()
        if not admin:
            db.close()
            return jsonify({'error': 'Admin not found'}), 404
        admin.password = generate_password_hash(new_password)
        db.commit()
        db.close()
        return jsonify({'message': 'Password updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
