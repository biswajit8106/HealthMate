from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from database.db import Base, engine

class Diagnosis(Base):
    __tablename__ = 'diagnoses'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    description = Column(String(255))
    symptoms = Column(String(255))
    treatment = Column(String(255))

    def __init__(self, name, description, symptoms, treatment):
        self.name = name
        self.description = description
        self.symptoms = symptoms
        self.treatment = treatment

    @staticmethod
    def create_table():
        Base.metadata.create_all(bind=engine)

    @staticmethod
    def add_diagnosis(db: Session, diagnosis):
        db.add(diagnosis)
        db.commit()
        db.refresh(diagnosis)
        return diagnosis

    @staticmethod
    def get_all_diagnoses(db: Session):
        return db.query(Diagnosis).all()
