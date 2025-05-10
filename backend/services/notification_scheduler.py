import json
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from firebase_admin import messaging, credentials, initialize_app
from database.db import SessionLocal
from models.medication_reminder_model import MedicationReminder
from sqlalchemy import text
import os

# Initialize Firebase Admin SDK
# Use raw string or forward slashes for Windows path to avoid escape sequence issues
cred_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'healthmate-413a7-firebase-adminsdk-fbsvc-c836b22bd7.json')
cred = credentials.Certificate(cred_path)
initialize_app(cred)

def send_push_notification(token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )
    response = messaging.send(message)
    print(f'Successfully sent message: {response}')

def check_and_send_notifications():
    import logging
    db = SessionLocal()
    try:
        now = datetime.datetime.now()
        current_time_str = now.strftime('%H:%M')
        current_date_str = now.strftime('%Y-%m-%d')

        logging.info(f"Checking notifications at {current_time_str} on {current_date_str}")

        # Query reminders active today
        reminders = db.query(MedicationReminder).filter(
            MedicationReminder.start_date <= current_date_str,
            MedicationReminder.end_date >= current_date_str
        ).all()

        logging.info(f"Found {len(reminders)} active reminders")

        for reminder in reminders:
            reminder_times = json.loads(reminder.reminder_times)
            logging.info(f"Reminder {reminder.id} times: {reminder_times}")
            if current_time_str in reminder_times:
                logging.info(f"Time match for reminder {reminder.id}")
                # Get user's FCM token
                token_row = db.execute(
                    text("SELECT token FROM fcm_tokens WHERE user_id = :user_id"),
                    {'user_id': reminder.user_id}
                ).fetchone()
                if token_row:
                    token = token_row[0]
                    title = 'Medicine Reminder'
                    body = f"Time to take your medicine: {reminder.medicine_name} - {reminder.dosage}"
                    try:
                        send_push_notification(token, title, body)
                    except Exception as e:
                        logging.error(f"Failed to send notification for reminder {reminder.id}: {e}")
            else:
                logging.info(f"No time match for reminder {reminder.id}")
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_and_send_notifications, 'interval', minutes=1)
    scheduler.start()
    print("Notification scheduler started.")

    try:
        import time
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if __name__ == '__main__':
    start_scheduler()
