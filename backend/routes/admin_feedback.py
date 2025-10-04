from fastapi import APIRouter, Depends, HTTPException
from utils.auth import get_current_admin
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# For demonstration, using in-memory store. In production, use persistent storage.
feedback_store = []

class ReplyRequest(BaseModel):
    reply: str

@router.get('/')
def list_feedback(admin_id: int = Depends(get_current_admin)):
    try:
        # For now, return all feedback from in-memory store
        return feedback_store
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/reply/{feedback_id}')
def reply_feedback(feedback_id: int, request_data: ReplyRequest, admin_id: int = Depends(get_current_admin)):
    try:
        if not request_data.reply:
            raise HTTPException(status_code=400, detail='Reply content required')
        # Find feedback and add reply
        for fb in feedback_store:
            if fb.get('id') == feedback_id:
                fb['reply'] = request_data.reply
                fb['resolved'] = True
                return {'message': 'Reply added and feedback marked resolved'}
        raise HTTPException(status_code=404, detail='Feedback not found')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/mark_resolved/{feedback_id}')
def mark_resolved(feedback_id: int, admin_id: int = Depends(get_current_admin)):
    try:
        for fb in feedback_store:
            if fb.get('id') == feedback_id:
                fb['resolved'] = True
                return {'message': 'Feedback marked resolved'}
        raise HTTPException(status_code=404, detail='Feedback not found')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
