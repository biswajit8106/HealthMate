from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.user_model import User

admin_auth_bp = Blueprint('admin_auth_bp', __name__, url_prefix='/admin/auth')

import traceback
from flask import current_app

@admin_auth_bp.route('/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400

    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email, User.is_admin == True).first()
        if user and check_password_hash(user.password, password):
            session['admin_user_id'] = user.user_id
            session.permanent = True
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
    except Exception as e:
        current_app.logger.error(f"Exception during admin login: {e}")
        current_app.logger.error(traceback.format_exc())
        db.rollback()
        return jsonify({'success': False, 'message': 'Internal server error'}), 500
    finally:
        db.close()

@admin_auth_bp.route('/logout', methods=['POST'])
def admin_logout():
    session.pop('admin_user_id', None)
    return jsonify({'success': True, 'message': 'Logout successful'})
