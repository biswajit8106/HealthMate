import os
from dotenv import load_dotenv

# Load .env file from backend directory
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Production flags
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')

    # Paths for ML model training (optional, relative)
    TRAINING_DATA_PATH = os.path.join('Training', 'Data', 'Training.csv').replace('\\', '/')
    MODEL_SAVE_PATH = os.path.join('models', 'trained_model.pkl').replace('\\', '/')

# Security
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key-here')
JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # 1 hour

# API Keys
INFERMEDICA_APP_ID = os.getenv('INFERMEDICA_APP_ID')
INFERMEDICA_APP_KEY = os.getenv('INFERMEDICA_APP_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
