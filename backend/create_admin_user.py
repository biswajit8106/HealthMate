from werkzeug.security import generate_password_hash
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.user_model import User

def create_admin_user(name, email, age, gender, password):
    db: Session = SessionLocal()
    try:
        hashed_password = generate_password_hash(password)
        admin_user = User(
            name=name,
            email=email,
            age=age,
            gender=gender,
            password=hashed_password,
            is_admin=True
        )
        db.add(admin_user)
        db.commit()
        print(f"Admin user '{email}' created successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error creating admin user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Replace these values with desired admin user details
    name = "Admin User"
    email = "admin@gmail.com"
    age = 30
    gender = "Other"
    password = "123456"

    create_admin_user(name, email, age, gender, password)
