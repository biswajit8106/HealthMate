from flask import Blueprint, request, jsonify, session
from database.db import get_db
from models.user_model import User
from sqlalchemy.orm import Session
from utils.auth import login_required


# Initialize Blueprint
profile_bp = Blueprint('profile_bp', __name__, url_prefix='/api/user/profile')

# GET: Fetch user profile
@profile_bp.route('', methods=['GET'], strict_slashes=False)
@profile_bp.route('/', methods=['GET'], strict_slashes=False)
@login_required
def get_profile():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    db: Session = next(get_db())
    user = User.get_user_by_id(db, user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_data = {
        'user_id': user.user_id,
        'name': user.name,
        'email': user.email,
        'age': user.age,
        'gender': user.gender
    }

    return jsonify(user_data), 200


# PUT: Update user profile
@profile_bp.route('', methods=['PUT'], strict_slashes=False)
@profile_bp.route('/', methods=['PUT'], strict_slashes=False)
@login_required
def update_profile():
    data = request.get_json()
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    db: Session = next(get_db())
    user = User.get_user_by_id(db, user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Update fields if provided
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.age = data.get('age', user.age)
    user.gender = data.get('gender', user.gender)

    # Optionally update password (should hash it!)
    if 'password' in data:
        from werkzeug.security import generate_password_hash
        user.password = generate_password_hash(data['password'])

    try:
        db.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
