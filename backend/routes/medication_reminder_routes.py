from flask import Blueprint, request, jsonify
from database.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
import json
from models.medication_reminder_model import MedicationReminder
from models.user_model import User

medication_reminder_bp = Blueprint('medication_reminder_bp', __name__, url_prefix='/api')

@medication_reminder_bp.route('/medication-reminder', methods=['POST'])
def add_medication_reminder():
    data = request.get_json()
    user_id = data.get('user_id')
    medicine_name = data.get('medicineName')
    dosage = data.get('dosage')
    reminder_times = data.get('reminderTimes')
    frequency = data.get('frequency')
    start_date = data.get('startDate')
    end_date = data.get('endDate')

    if not all([user_id, medicine_name, dosage, reminder_times, frequency, start_date, end_date]):
        return jsonify({'error': 'Missing required fields'}), 400

    db = next(get_db())
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
        return jsonify({'message': 'Medication reminder added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@medication_reminder_bp.route('/medication-reminder', methods=['GET'])
def get_medication_reminders():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'Missing user_id parameter'}), 400

    db = next(get_db())
    try:
        reminders = MedicationReminder.get_reminders_by_user(db, int(user_id))
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
        return jsonify({'reminders': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@medication_reminder_bp.route('/save-fcm-token', methods=['POST'])
def save_fcm_token():
    import logging
    data = request.get_json()
    user_id = data.get('user_id')
    token = data.get('token')

    if not user_id or not token:
        return jsonify({'error': 'Missing user_id or token'}), 400

    db = next(get_db())
    try:
        # Upsert token for user
        existing = db.execute(text("SELECT * FROM fcm_tokens WHERE user_id = :user_id"), {'user_id': user_id}).fetchone()
        if existing:
            db.execute(text("UPDATE fcm_tokens SET token = :token WHERE user_id = :user_id"), {'token': token, 'user_id': user_id})
        else:
            db.execute(text("INSERT INTO fcm_tokens (user_id, token) VALUES (:user_id, :token)"), {'user_id': user_id, 'token': token})
        db.commit()
        return jsonify({'message': 'FCM token saved successfully'}), 200
    except Exception as e:
        logging.error(f"Error saving FCM token: {e}")
        return jsonify({'error': str(e)}), 500

@medication_reminder_bp.route('/delete-fcm-token', methods=['POST'])
def delete_fcm_token():
    import logging
    data = request.get_json()
    user_id = data.get('user_id')
    token = data.get('token')

    if not user_id or not token:
        return jsonify({'error': 'Missing user_id or token'}), 400

    db = next(get_db())
    try:
        db.execute(text("DELETE FROM fcm_tokens WHERE user_id = :user_id AND token = :token"), {'user_id': user_id, 'token': token})
        db.commit()
        return jsonify({'message': 'FCM token deleted successfully'}), 200
    except Exception as e:
        logging.error(f"Error deleting FCM token: {e}")
        return jsonify({'error': str(e)}), 500
