from dateutil import parser
from models.medication_reminder_model import MedicationReminder

def delete_expired_reminders(db):
    import datetime
    expired_reminders = []
    now = datetime.datetime.now()
    reminders = db.query(MedicationReminder).all()
    for reminder in reminders:
        try:
            end_date_dt = parser.parse(reminder.end_date)
        except Exception:
            continue
        if end_date_dt <= now:
            expired_reminders.append(reminder)
    for reminder in expired_reminders:
        db.delete(reminder)
    db.commit()
    return len(expired_reminders)
