from fastapi import APIRouter, Depends, HTTPException
from utils.auth import get_current_admin
from pydantic import BaseModel
import datetime

router = APIRouter()

# For demonstration, using in-memory logs. In production, use persistent storage.
activity_logs = []
failed_login_attempts = []
admin_login_ips = {}

class RecordIPRequest(BaseModel):
    admin_id: int
    ip: str

@router.get('/activity')
def get_activity_logs(admin_id: int = Depends(get_current_admin)):
    try:
        # Return last 100 activity logs
        return activity_logs[-100:]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/failed_logins')
def get_failed_logins(admin_id: int = Depends(get_current_admin)):
    try:
        # Return last 100 failed login attempts
        return failed_login_attempts[-100:]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/login_ip')
def record_login_ip(request_data: RecordIPRequest, admin_id: int = Depends(get_current_admin)):
    try:
        admin_login_ips.setdefault(request_data.admin_id, []).append({'ip': request_data.ip, 'timestamp': datetime.datetime.utcnow().isoformat()})
        return {'message': 'IP recorded'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/session_management')
def get_sessions(admin_id: int = Depends(get_current_admin)):
    try:
        # Placeholder for session management data
        sessions = [
            {'session_id': 'abc123', 'admin_id': 1, 'login_time': '2024-01-01T12:00:00Z', 'active': True},
            {'session_id': 'def456', 'admin_id': 2, 'login_time': '2024-01-02T08:30:00Z', 'active': False},
        ]
        return sessions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
