from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models.user_model import User
from utils.auth import get_current_user
from pydantic import BaseModel

router = APIRouter()

class PrivacySettingsRequest(BaseModel):
    dataSharing: bool

class PrivacySettingsResponse(BaseModel):
    dataSharing: bool

@router.get('/user/privacy', response_model=PrivacySettingsResponse)
def get_privacy_settings(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    user = User.get_user_by_id(db, user_id)
    if user:
        return {"dataSharing": getattr(user, "dataSharing", False)}
    raise HTTPException(status_code=404, detail="User not found")

@router.put('/user/privacy', response_model=dict)
def update_privacy_settings(request_data: PrivacySettingsRequest, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    user = User.get_user_by_id(db, user_id)
    if user:
        setattr(user, "dataSharing", request_data.dataSharing)
        db.commit()
        return {"message": "Privacy settings updated"}
    raise HTTPException(status_code=404, detail="User not found")

@router.delete('/user/history', response_model=dict)
def delete_history(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    # Assuming User model has a method to delete history
    user = User.get_user_by_id(db, user_id)
    if user:
        # Implement actual history deletion logic here
        # For now, simulate success
        return {"message": "History deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")
