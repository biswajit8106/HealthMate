from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db import Base

class MedicineReminder(Base):
    __tablename__ = 'medicine_reminders'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    medicine_name = Column(String(255), nullable=False)
    dosage = Column(String(255), nullable=True)
    timing = Column(String(255), nullable=True)
    frequency = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="medication_reminders")

# Add back_populates in User model (in user_model.py) if not already present:
# medicine_reminders = relationship("MedicineReminder", back_populates="user")
