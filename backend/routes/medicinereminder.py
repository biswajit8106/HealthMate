from flask import Blueprint, request, jsonify, session
from sqlalchemy.orm import Session
import traceback
from database.db import SessionLocal
from models.medicine_reminder_model import  MedicineReminder
from models.push_subscription_model import PushSubscription
from utils.auth import login_required
from services.push_notification_service import send_push_notification
from services.email_notification_service import send_email
from datetime import datetime

medicinereminder_bp = Blueprint('medicinereminder', __name__)

@medicinereminder_bp.route('/reminder', methods=['POST'])
@login_required
def add_medicine_reminder():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not logged in'}), 401

        data = request.get_json()
        medicine_name = data.get('medicine_name')
        dosage = data.get('dosage')
        timing = data.get('timing')
        frequency = data.get('frequency')
        notes = data.get('notes')
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')

        if not medicine_name or not start_date_str:
            return jsonify({'error': 'medicine_name and start_date are required'}), 400

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

        db: Session = SessionLocal()
        reminder = MedicineReminder(
            user_id=user_id,
            medicine_name=medicine_name,
            dosage=dosage,
            timing=timing,
            frequency=frequency,
            notes=notes,
            start_date=start_date,
            end_date=end_date
        )
        db.add(reminder)
        db.commit()
        db.refresh(reminder)
        db.close()

        return jsonify({'message': 'Medicine reminder added successfully', 'reminder_id': reminder.id}), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@medicinereminder_bp.route('/reminder', methods=['GET'])
@login_required
def get_medicine_reminders():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not logged in'}), 401

        db: Session = SessionLocal()
        reminders = db.query(MedicineReminder).filter_by(user_id=user_id).all()
        db.close()

        reminder_list = []
        for r in reminders:
            reminder_list.append({
                'id': r.id,
                'medicine_name': r.medicine_name,
                'dosage': r.dosage,
                'timing': r.timing,
                'frequency': r.frequency,
                'notes': r.notes,
                'start_date': r.start_date.isoformat(),
                'end_date': r.end_date.isoformat() if r.end_date else None,
                'created_at': r.created_at.isoformat(),
                'updated_at': r.updated_at.isoformat()
            })

        return jsonify(reminder_list), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@medicinereminder_bp.route('/reminder/history', methods=['GET'])
@login_required
def get_medicine_reminder_history():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not logged in'}), 401

        # For simplicity, returning all reminders as history for now
        db: Session = SessionLocal()
        reminders = db.query(MedicineReminder).filter_by(user_id=user_id).all()
        db.close()

        history_list = []
        for r in reminders:
            history_list.append({
                'id': r.id,
                'medicine_name': r.medicine_name,
                'dosage': r.dosage,
                'timing': r.timing,
                'frequency': r.frequency,
                'notes': r.notes,
                'start_date': r.start_date.isoformat(),
                'end_date': r.end_date.isoformat() if r.end_date else None,
                'created_at': r.created_at.isoformat(),
                'updated_at': r.updated_at.isoformat()
            })

        return jsonify(history_list), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@medicinereminder_bp.route('/subscribe', methods=['POST'])
@login_required
def subscribe_push():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not logged in'}), 401

        subscription_json = request.get_json()
        if not subscription_json:
            return jsonify({'error': 'No subscription data provided'}), 400

        import logging
        logging.info(f"Received subscription JSON: {subscription_json}")

        db: Session = SessionLocal()
        existing_subscription = db.query(PushSubscription).filter_by(user_id=user_id).first()

        if existing_subscription:
            existing_subscription.subscription_info = json.dumps(subscription_json)
        else:
            new_subscription = PushSubscription(
                user_id=user_id,
                subscription_info=json.dumps(subscription_json)
            )
            db.add(new_subscription)

        db.commit()
        db.close()

        return jsonify({'message': 'Push subscription saved successfully'}), 201

    except Exception as e:
        import logging
        logging.error(f"Error saving push subscription: {e}", exc_info=True)
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@medicinereminder_bp.route('/send_push', methods=['POST'])
@login_required
def send_push():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not logged in'}), 401

        data = request.get_json()
        payload = data.get('payload', {'title': 'Test Notification', 'body': 'This is a test push notification.'})

        success = send_push_notification(user_id, payload)
        if success:
            return jsonify({'message': 'Push notification sent successfully'}), 200
        else:
            return jsonify({'error': 'Failed to send push notification'}), 500

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
