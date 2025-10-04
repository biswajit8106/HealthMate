from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models.user_model import User
from utils.auth import get_current_admin
from werkzeug.security import generate_password_hash
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class AddAdminRequest(BaseModel):
    name: str
    email: str
    password: str
    role: Optional[str] = 'Moderator'

class ChangeRoleRequest(BaseModel):
    role: str

class ChangePasswordRequest(BaseModel):
    password: str

@router.get('/admins')
def list_admins(admin_id: int = Depends(get_current_admin), db: Session = Depends(get_db)):
    try:
        admins = db.query(User).filter(User.is_admin == True).all()
        admins_data = []
        for admin in admins:
            admins_data.append({
                'user_id': admin.user_id,
                'name': admin.name,
                'email': admin.email,
                'role': admin.role if hasattr(admin, 'role') else 'Moderator',
            })
        return admins_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/admins')
def add_admin(request_data: AddAdminRequest, admin_id: int = Depends(get_current_admin), db: Session = Depends(get_db)):
    try:
        existing = db.query(User).filter(User.email == request_data.email).first()
        if existing:
            raise HTTPException(status_code=400, detail='Admin with this email already exists')

        hashed_password = generate_password_hash(request_data.password)
        new_admin = User(name=request_data.name, email=request_data.email, password=hashed_password, is_admin=True, role=request_data.role)
        db.add(new_admin)
        db.commit()
        return {'message': 'Admin added successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete('/admins/{user_id}')
def remove_admin(user_id: int, admin_id: int = Depends(get_current_admin), db: Session = Depends(get_db)):
    try:
        admin = db.query(User).filter(User.user_id == user_id, User.is_admin == True).first()
        if not admin:
            raise HTTPException(status_code=404, detail='Admin not found')
        db.delete(admin)
        db.commit()
        return {'message': 'Admin removed successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put('/admins/{user_id}/role')
def change_role(user_id: int, request_data: ChangeRoleRequest, admin_id: int = Depends(get_current_admin), db: Session = Depends(get_db)):
    try:
        admin = db.query(User).filter(User.user_id == user_id, User.is_admin == True).first()
        if not admin:
            raise HTTPException(status_code=404, detail='Admin not found')
        admin.role = request_data.role
        db.commit()
        return {'message': 'Role updated successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put('/admins/{user_id}/password')
def change_password(user_id: int, request_data: ChangePasswordRequest, admin_id: int = Depends(get_current_admin), db: Session = Depends(get_db)):
    try:
        admin = db.query(User).filter(User.user_id == user_id, User.is_admin == True).first()
        if not admin:
            raise HTTPException(status_code=404, detail='Admin not found')
        admin.password = generate_password_hash(request_data.password)
        db.commit()
        return {'message': 'Password updated successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
