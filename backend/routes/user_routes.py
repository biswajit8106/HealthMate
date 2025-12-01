from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from models.user_model import User
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db
from sqlalchemy.orm import Session
from utils.auth import get_current_user
from pydantic import BaseModel

router = APIRouter()

class RegisterRequest(BaseModel):
    username: str
    email: str
    age: int
    gender: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post('/register', status_code=201)
def register(request_data: RegisterRequest, db: Session = Depends(get_db)):
    data = request_data.dict()
    
    # Validate required fields
    required_fields = ['username', 'email', 'age', 'gender', 'password']
    if not all(field in data for field in required_fields):
        raise HTTPException(status_code=400, detail="Missing required fields")

    hashed_password = generate_password_hash(data['password'])

    new_user = User(
        name=data['username'],
        email=data['email'],
        age=data['age'],
        gender=data['gender'],
        password=hashed_password
    )

    result = User.add_user(db, new_user)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"message": "User registered successfully!"}

@router.post('/login')
def login(request_data: LoginRequest, response: Response, db: Session = Depends(get_db)):
    data = request_data.dict()
    
    if 'email' not in data or 'password' not in data:
        raise HTTPException(status_code=400, detail="Email and password are required")

    user = User.get_user_by_email(db, data['email'])

    if user and check_password_hash(user.password, data['password']):
        # Set cookie for session-like behavior
        response.set_cookie(key="user_id", value=str(user.user_id), httponly=True, secure=True, samesite="none")
        user_data = {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "age": user.age,
            "gender": user.gender
        }
        return {"message": "Login successful!", "user": user_data}

    raise HTTPException(status_code=401, detail="Invalid email or password!")

@router.post('/logout')
def logout(response: Response):
    response.delete_cookie(key="user_id")
    return {"message": "Logout successful!"}

@router.get('/session')
def session_info(user_id: int = Cookie(None), db: Session = Depends(get_db)):
    if user_id:
        user = User.get_user_by_id(db, user_id)
        if user:
            user_data = {
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email,
                "age": user.age,
                "gender": user.gender
            }
            return {"logged_in": True, "user": user_data}
    return {"logged_in": False}
