from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from database.db import Base, engine

class Disease(Base):
    __tablename__ = 'diseases'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    description = Column(String(255))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    @staticmethod
    def create_table():
        Base.metadata.create_all(bind=engine)

    @staticmethod
    def add_disease(db: Session, disease):
        db.add(disease)
        db.commit()
        db.refresh(disease)
        return disease

    @staticmethod
    def get_all_diseases(db: Session):
        return db.query(Disease).all()
