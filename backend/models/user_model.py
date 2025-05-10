from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Session, relationship
from database.db import Base, engine
import datetime

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    age = Column(Integer)
    gender = Column(String(10))
    password = Column(String(255))
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

   
    # Use string-based lazy relationship to avoid circular import issues


    def __init__(self, name, email, age, gender, password, is_admin=False, is_active=True, is_deleted=False):
        self.name = name
        self.email = email
        self.age = age
        self.gender = gender
        self.password = password
        self.is_admin = is_admin
        self.is_active = is_active
        self.is_deleted = is_deleted

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.user_id == user_id).first()

    @staticmethod
    def create_table():
        Base.metadata.create_all(bind=engine)

    @staticmethod
    def add_user(db: Session, user):
        db.add(user)
        try:
            db.commit()
            db.refresh(user)
            return user
        except Exception as e:
            db.rollback()
            if "Duplicate entry" in str(e):
                return {"error": "User already registered."}
            raise e

    @staticmethod
    def get_all_users(db: Session):
        return db.query(User).all()
