# AI Doctor Backend

## Overview
This is the backend service for the AI Doctor application, built with Flask and MySQL. It provides APIs for:
- User authentication
- Symptom checking
- Disease prediction
- Medicine recommendation

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables in the `.env` file located in the `backend` directory. Example `.env` content:
```env
# Flask secret key for session management and security
SECRET_KEY=your-secret-key-here

# JWT secret key for token encoding and decoding
JWT_SECRET_KEY=your-jwt-secret-key-here

# JWT access token expiration time in seconds (default 3600 seconds = 1 hour)
JWT_ACCESS_TOKEN_EXPIRES=3600

# Database connection URL (e.g., mysql+pymysql://user:password@host/dbname)
DATABASE_URL=mysql+pymysql://root:password@localhost/healthmate

# Infermedica API credentials for symptom checker integration
INFERMEDICA_APP_ID=your-infermedica-app-id-here
INFERMEDICA_APP_KEY=your-infermedica-app-key-here

# Path to Firebase service account JSON file
FIREBASE_SERVICE_ACCOUNT_JSON_PATH=backend/services/healthmate-413a7-firebase-adminsdk-fbsvc-c836b22bd7.json
```

3. Run the application:
```bash
python run.py
```

## API Endpoints

### User Authentication
- POST `/register` - Register a new user

### Symptom Diagnosis
- POST `/check` - Check symptoms and get diagnosis

### Medicine Recommendation
- POST `/recommend` - Get medicine recommendation
