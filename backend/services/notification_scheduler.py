import json
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from firebase_admin import messaging, credentials, initialize_app
from database.db import SessionLocal
from models.medication_reminder_model import MedicationReminder
from sqlalchemy import text
import os
from models.medication_reminder_model_extension import delete_expired_reminders as delete_expired_reminders_func
import logging
from models.user_model import User
from utils.email_utils import send_email
from config import Config




# Initialize Firebase Admin SDK using environment variables
firebase_initialized = False
try:
    firebase_config = {
        "type": "service_account",
        "project_id": Config.FIREBASE_PROJECT_ID,
        "private_key_id": Config.FIREBASE_PRIVATE_KEY_ID,
        "private_key": Config.FIREBASE_PRIVATE_KEY.replace('\\n', '\n') if Config.FIREBASE_PRIVATE_KEY else None,
        "client_email": Config.FIREBASE_CLIENT_EMAIL,
        "client_id": Config.FIREBASE_CLIENT_ID,
        "auth_uri": Config.FIREBASE_AUTH_URI,
        "token_uri": Config.FIREBASE_TOKEN_URI,
        "auth_provider_x509_cert_url": Config.FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
        "client_x509_cert_url": Config.FIREBASE_CLIENT_X509_CERT_URL
    }

    if all(firebase_config.values()):
        cred = credentials.Certificate(firebase_config)
        initialize_app(cred)
        firebase_initialized = True
        logging.info("Firebase Admin SDK initialized successfully using environment variables.")
    else:
        logging.warning("Firebase credentials not fully configured in environment variables. Push notifications will be disabled.")
except Exception as e:
    logging.error(f"Failed to initialize Firebase Admin SDK: {e}")

def send_push_notification(token, title, body):
    if not firebase_initialized:
        logging.warning("Firebase not initialized. Skipping push notification.")
        return

    if not token:
        logging.warning("No FCM token provided. Skipping push notification.")
        return

    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
        )
        response = messaging.send(message)
        logging.info(f'Successfully sent push notification: {response}')
    except messaging.UnregisteredError as e:
        logging.error(f"FCM token is unregistered or invalid for reminder: {e}. Consider removing this token.")
    except messaging.SenderIdMismatchError as e:
        logging.error(f"SenderId mismatch for FCM token: {e}. Check Firebase project configuration and token validity.")
    except Exception as e:
        logging.error(f"Failed to send push notification: {e}")
    


def check_and_send_notifications():
   
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
            reminder_times = json.loads(str(reminder.reminder_times))
            logging.info(f"Reminder {reminder.id} times: {reminder_times}")
            if current_time_str in reminder_times:
                logging.info(f"Time match for reminder {reminder.id}")
                # Get user's FCM token
                token_row = db.execute(
                    text("SELECT token FROM fcm_tokens WHERE user_id = :user_id"),
                    {'user_id': reminder.user_id}
                ).fetchone()
                # Get user's email
                user = User.get_user_by_id(db, reminder.user_id)  # type: ignore
                if user:
                    user_name = user.name or 'User'
                    user_email = user.email
                    title = 'Medicine Reminder'
                    body = f"Hey {user_name} take your medicine {reminder.medicine_name} {reminder.dosage} this is the time to take your medicine don't forget take your medicine now"
                    if token_row:
                        token = token_row[0]
                        try:
                            send_push_notification(token, title, body)
                        except Exception as e:
                            logging.error(f"Failed to send notification for reminder {reminder.id}: {e}")
                    if user_email:  # type: ignore
                        try:
                            send_email(user_email, title, body)
                        except Exception as e:
                            logging.error(f"Failed to send email for reminder {reminder.id} to {user_email}: {e}")
            else:
                logging.info(f"No time match for reminder {reminder.id}")
    finally:
        db.close()
# Schedule the deletion of expired reminders
def delete_expired_reminders():
    db = SessionLocal()
    try:
        deleted_count = delete_expired_reminders_func(db)
        logging.info(f"Deleted {deleted_count} expired medication reminders.")
    except Exception as e:
        logging.error(f"Error deleting expired medication reminders: {e}")
    finally:
        db.close()

# In the start_scheduler() function, add this line to schedule the deletion job:

    

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_and_send_notifications, 'interval', minutes=1)
    scheduler.add_job(delete_expired_reminders, 'interval', hours=24)
    scheduler.start()
    print("Notification scheduler started.")

if __name__ == '__main__':
    start_scheduler()
