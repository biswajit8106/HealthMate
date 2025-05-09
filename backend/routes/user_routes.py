from flask import Blueprint, request, jsonify, session
from models.user_model import User
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint('user_bp', __name__)

from database.db import get_db
from sqlalchemy.orm import Session

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['username', 'email', 'age', 'gender', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    hashed_password = generate_password_hash(data['password'])

    new_user = User(
        name=data['username'],
        email=data['email'],
        age=data['age'],
        gender=data['gender'],
        password=hashed_password
    )

    db: Session = next(get_db())
    result = User.add_user(db, new_user)
    if isinstance(result, dict) and "error" in result:
        return jsonify({"message": result["error"]}), 400
    return jsonify({"message": "User registered successfully!"}), 201


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if 'email' not in data or 'password' not in data:
        return jsonify({"message": "Email and password are required"}), 400

    db: Session = next(get_db())
    user = User.get_user_by_email(db, data['email'])

    if user and check_password_hash(user.password, data['password']):
        session['user_id'] = user.user_id
        session.permanent = True
        session.modified = True
        user_data = {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "age": user.age,
            "gender": user.gender
        }
        response = jsonify({"message": "Login successful!", "user": user_data})
        # Log response headers for debugging
        print("Response headers before return:", response.headers)
        # Log Set-Cookie header if present
        if 'Set-Cookie' in response.headers:
            print("Set-Cookie header:", response.headers['Set-Cookie'])
        else:
            print("No Set-Cookie header found in response")
        return response

    return jsonify({"message": "Invalid email or password!"}), 401


@user_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logout successful!"}), 200

@user_bp.route('/session', methods=['GET'])
def session_info():
    if 'user_id' in session:
        db: Session = next(get_db())
        user = User.get_user_by_id(db, session['user_id'])
        if user:
            user_data = {
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email,
                "age": user.age,
                "gender": user.gender
            }
            return jsonify({"logged_in": True, "user": user_data})
    return jsonify({"logged_in": False, "message": "No active session"}), 401
