from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time
from services.push_notification_service import send_push_notification
from database.db import SessionLocal
from models.medicine_reminder_model import MedicineReminder
from models.user_model import User

def send_email(to_email, subject, body):
    # Configure your SMTP server credentials here
    smtp_server = "smtp.example.com"
    smtp_port = 587
    smtp_username = "your_email@example.com"
    smtp_password = "your_email_password"

    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to_email, msg.as_string())
        server.quit()
        print(f"Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        return False

def check_and_send_reminders():
    now = datetime.utcnow()
    current_time_str = now.strftime("%H:%M")
    current_time_obj = datetime.strptime(current_time_str, "%H:%M").time()
    today = now.date()
    db = SessionLocal()
    try:
        reminders = db.query(MedicineReminder).filter(
            MedicineReminder.start_date <= today,
            (MedicineReminder.end_date == None) | (MedicineReminder.end_date >= today)
        ).all()

        for reminder in reminders:
            if not reminder.timing:
                continue
            # timing may contain multiple times separated by commas
            times = [t.strip() for t in reminder.timing.split(',')]
            for t in times:
                try:
                    reminder_time_obj = datetime.strptime(t, "%H:%M").time()
                    # Check if current time matches reminder time (within 1 minute)
                    if abs(datetime.combine(today, reminder_time_obj) - datetime.combine(today, current_time_obj)).seconds < 60:
                        # Send push notification
                        send_push_notification(reminder.user_id, {
                            "title": "Medication Reminder",
                            "body": f"Time to take your medication: {reminder.medicine_name}"
                        })

                        # Send email notification
                        user = db.query(User).filter(User.id == reminder.user_id).first()
                        if user and user.email:
                            subject = "Medication Reminder"
                            body = f"Dear {user.username},\n\nThis is a reminder to take your medication: {reminder.medicine_name} at {t}.\n\nBest regards,\nYour Health App"
                            send_email(user.email, subject, body)
                except Exception as e:
                    print(f"Error parsing reminder time '{t}': {e}")

    except Exception as e:
        print(f"Error sending reminders: {e}")
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_and_send_reminders, trigger="interval", minutes=1)
    scheduler.start()
    print("Reminder scheduler started.")

    import atexit
    atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    start_scheduler()
    import time
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        pass
