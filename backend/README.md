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

2. Configure environment variables in `.env`:
```env
DATABASE_URL=mysql+pymysql://root:password@localhost/healthmate
SECRET_KEY=your-secret-key
INFERMEDICA_APP_ID=your-app-id
INFERMEDICA_APP_KEY=your-app-key
```

3. Run the application:
```bash
python run.py
```

## API Endpoints

### User Authentication
- POST `/register` - Register a new user

### Symptom Checker
- POST `/check` - Check symptoms and get diagnosis

### Medicine Recommendation
- POST `/recommend` - Get medicine recommendation
