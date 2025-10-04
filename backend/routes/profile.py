from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models.user_model import User
from utils.auth import get_current_user
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    password: Optional[str] = None

# GET: Fetch user profile
@router.get('')
@router.get('/')
def get_profile(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    user = User.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    user_data = {
        'user_id': user.user_id,
        'name': user.name,
        'email': user.email,
        'age': user.age,
        'gender': user.gender
    }

    return user_data


# PUT: Update user profile
@router.put('')
@router.put('/')
def update_profile(request_data: UpdateProfileRequest, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    user = User.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    # Update fields if provided
    if request_data.name is not None:
        user.name = request_data.name
    if request_data.email is not None:
        user.email = request_data.email
    if request_data.age is not None:
        user.age = request_data.age
    if request_data.gender is not None:
        user.gender = request_data.gender

    # Optionally update password (should hash it!)
    if request_data.password:
        from werkzeug.security import generate_password_hash
        user.password = generate_password_hash(request_data.password)

    try:
        db.commit()
        return {'message': 'Profile updated successfully'}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
