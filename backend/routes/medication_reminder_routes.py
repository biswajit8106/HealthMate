from fastapi import APIRouter, Depends, HTTPException
from database.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
import json
from models.medication_reminder_model import MedicationReminder
from models.user_model import User
from pydantic import BaseModel
from typing import List

router = APIRouter()

class AddReminderRequest(BaseModel):
    user_id: int
    medicineName: str
    dosage: str
    reminderTimes: List[str]
    frequency: str
    startDate: str
    endDate: str

class SaveTokenRequest(BaseModel):
    user_id: int
    token: str

@router.post('/medication-reminder', status_code=201)
def add_medication_reminder(request_data: AddReminderRequest, db: Session = Depends(get_db)):
    data = request_data.dict()
    user_id = data.get('user_id')
    medicine_name = data.get('medicineName')
    dosage = data.get('dosage')
    reminder_times = data.get('reminderTimes')
    frequency = data.get('frequency')
    start_date = data.get('startDate')
    end_date = data.get('endDate')

    if not all([user_id, medicine_name, dosage, reminder_times, frequency, start_date, end_date]):
        raise HTTPException(status_code=400, detail='Missing required fields')

    try:
        reminder = MedicationReminder(
            user_id=user_id,
            medicine_name=medicine_name,
            dosage=dosage,
            reminder_times=json.dumps(reminder_times),
            frequency=frequency,
            start_date=start_date,
            end_date=end_date
        )
        MedicationReminder.add_reminder(db, reminder)
        return {'message': 'Medication reminder added successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/medication-reminder')
def get_medication_reminders(user_id: int, db: Session = Depends(get_db)):
    if not user_id:
        raise HTTPException(status_code=400, detail='Missing user_id parameter')

    try:
        reminders = MedicationReminder.get_reminders_by_user(db, user_id)
        result = []
        for reminder in reminders:
            result.append({
                'id': reminder.id,
                'medicineName': reminder.medicine_name,
                'dosage': reminder.dosage,
                'reminderTimes': json.loads(reminder.reminder_times),
                'frequency': reminder.frequency,
                'startDate': reminder.start_date,
                'endDate': reminder.end_date,
            })
        return {'reminders': result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/save-fcm-token')
def save_fcm_token(request_data: SaveTokenRequest, db: Session = Depends(get_db)):
    import logging
    data = request_data.dict()
    user_id = data.get('user_id')
    token = data.get('token')

    if not user_id or not token:
        raise HTTPException(status_code=400, detail='Missing user_id or token')

    try:
        # Upsert token for user
        existing = db.execute(text("SELECT * FROM fcm_tokens WHERE user_id = :user_id"), {'user_id': user_id}).fetchone()
        if existing:
            db.execute(text("UPDATE fcm_tokens SET token = :token WHERE user_id = :user_id"), {'token': token, 'user_id': user_id})
        else:
            db.execute(text("INSERT INTO fcm_tokens (user_id, token) VALUES (:user_id, :token)"), {'user_id': user_id, 'token': token})
        db.commit()
        return {'message': 'FCM token saved successfully'}
    except Exception as e:
        logging.error(f"Error saving FCM token: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/delete-fcm-token')
def delete_fcm_token(request_data: SaveTokenRequest, db: Session = Depends(get_db)):
    import logging
    data = request_data.dict()
    user_id = data.get('user_id')
    token = data.get('token')

    if not user_id or not token:
        raise HTTPException(status_code=400, detail='Missing user_id or token')

    try:
        db.execute(text("DELETE FROM fcm_tokens WHERE user_id = :user_id AND token = :token"), {'user_id': user_id, 'token': token})
        db.commit()
        return {'message': 'FCM token deleted successfully'}
    except Exception as e:
        logging.error(f"Error deleting FCM token: {e}")
        raise HTTPException(status_code=500, detail=str(e))
