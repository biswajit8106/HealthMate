from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models.user_model import User
from utils.auth import get_current_admin
from pydantic import BaseModel
from typing import List

router = APIRouter()

class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str
    age: int
    gender: str
    is_active: bool
    is_admin: bool

@router.get('/', response_model=List[UserResponse])
def list_users(admin_id: int = Depends(get_current_admin), db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
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
        return users_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/activate/{user_id}', response_model=dict)
def activate_user(user_id: int, admin_id: int = Depends(get_current_admin), db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        user.is_active = True
        db.commit()
        return {'message': 'User activated successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/deactivate/{user_id}', response_model=dict)
def deactivate_user(user_id: int, admin_id: int = Depends(get_current_admin), db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        user.is_active = False
        db.commit()
        return {'message': 'User deactivated successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete('/delete/{user_id}', response_model=dict)
def delete_user(user_id: int, admin_id: int = Depends(get_current_admin), db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        # Soft delete: set is_active to False and mark deleted flag if exists
        user.is_active = False
        if hasattr(user, 'is_deleted'):
            user.is_deleted = True
        db.commit()
        return {'message': 'User deleted (soft) successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
