from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from database.db import Base
import datetime

class HealthReport(Base):
    __tablename__ = 'health_reports'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    name = Column(String(100))
    gender = Column(String(20))
    age = Column(Integer)
    predicted_disease = Column(String(100))
    confidence = Column(Float)
    description = Column(Text)
    symptoms = Column(Text)
    precautions = Column(Text)
    medications = Column(Text)
    diets = Column(Text)
    workouts = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
