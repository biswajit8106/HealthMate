from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Session
from database.db import Base, engine
import datetime
import json

class MedicationReminder(Base):
    __tablename__ = 'medication_reminders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    medicine_name = Column(String(255), nullable=False)
    dosage = Column(String(255), nullable=False)
    reminder_times = Column(String, nullable=False)  # JSON string of times
    frequency = Column(String(50), nullable=False)
    start_date = Column(String(50), nullable=False)
    end_date = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    @staticmethod
    def create_table():
        Base.metadata.create_all(bind=engine)

    @staticmethod
    def add_reminder(db: Session, reminder):
        db.add(reminder)
        try:
            db.commit()
            db.refresh(reminder)
            return reminder
        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def get_reminders_by_user(db: Session, user_id: int):
        return db.query(MedicationReminder).filter(MedicationReminder.user_id == user_id).all()
