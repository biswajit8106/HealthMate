from fastapi import APIRouter, Depends, HTTPException
from utils.auth import get_current_admin
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# In-memory settings store for demonstration
settings_store = {
    'max_file_size': 10485760,  # 10 MB
    'report_retention_days': 365,
    'ml_confidence_threshold': 0.8
}

class UpdateSettingsRequest(BaseModel):
    max_file_size: Optional[int] = None
    report_retention_days: Optional[int] = None
    ml_confidence_threshold: Optional[float] = None

@router.get('/')
def get_settings(admin_id: int = Depends(get_current_admin)):
    try:
        return settings_store
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put('/')
def update_settings(request_data: UpdateSettingsRequest, admin_id: int = Depends(get_current_admin)):
    try:
        for key, value in request_data.dict(exclude_unset=True).items():
            if key in settings_store:
                settings_store[key] = value
        return {'message': 'Settings updated successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
