from fastapi import APIRouter, Depends, HTTPException, Response
from werkzeug.security import check_password_hash
from sqlalchemy.orm import Session
from database.db import get_db
from models.user_model import User
from pydantic import BaseModel

router = APIRouter()

class AdminLoginRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    success: bool
    message: str

@router.post('/login', response_model=AuthResponse)
def admin_login(request_data: AdminLoginRequest, response: Response, db: Session = Depends(get_db)):
    if not request_data.email or not request_data.password:
        raise HTTPException(status_code=400, detail='Email and password are required')

    try:
        user = db.query(User).filter(User.email == request_data.email, User.is_admin == True).first()
        if user and check_password_hash(user.password, request_data.password):
            response.set_cookie(key='admin_user_id', value=str(user.user_id), httponly=True)
            return {'success': True, 'message': 'Login successful'}
        else:
            raise HTTPException(status_code=401, detail='Invalid email or password')
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal server error')

@router.post('/logout', response_model=AuthResponse)
def admin_logout(response: Response):
    response.delete_cookie(key='admin_user_id')
    return {'success': True, 'message': 'Logout successful'}
