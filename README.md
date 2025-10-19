# HealthMate

A comprehensive health management application that leverages machine learning for symptom checking, provides medication reminders, health report analysis, and administrative controls to empower users in managing their health effectively.

## Features

- **Symptom Checker**: Predict potential diseases based on user-reported symptoms using a trained machine learning model.
- **Medication Reminders**: Schedule and manage medication reminders with push notifications.
- **Health Reports**: Generate, save, and analyze health reports with detailed insights.
- **Medical History**: Track and manage personal medical history records.
- **Admin Panel**: Comprehensive administrative controls for user management, health reports, system logs, and settings.
- **Dashboard**: Visualize health data and analytics with interactive charts.
- **Report Analyzer**: Analyze medical reports using OCR and AI-powered processing.
- **Privacy Controls**: Manage user privacy settings and data sharing preferences.
- **Push Notifications**: Receive timely reminders via web push notifications using Firebase.

## Architecture

- **Backend**: FastAPI-based REST API with SQLAlchemy for database ORM, scikit-learn for machine learning predictions, and APScheduler for background tasks.
- **Frontend**: React application built with Create React App, featuring routing with React Router, data visualization with Recharts, and Firebase integration for notifications.
- **Database**: MySQL database with SQLAlchemy ORM for data persistence.
- **ML Model**: Pre-trained model for disease prediction from symptoms, stored in pickle format.

## Installation

### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- MySQL database server

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables by creating a `.env` file in the backend directory:
   ```env
   DATABASE_URL=mysql+pymysql://username:password@localhost/healthmate
   SECRET_KEY=your_secret_key_here
   CORS_ORIGINS=http://localhost:3000
   LOG_LEVEL=INFO
   ```

5. Initialize the database:
   ```bash
   python create_admin_user.py  # If needed for admin setup
   ```

6. Run the backend server:
   ```bash
   python run.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure Firebase (if using notifications) by updating `src/firebaseConfig.js` with your Firebase project credentials.

4. Start the development server:
   ```bash
   npm start
   ```

## Usage

1. Ensure the backend server is running on port 5000.
2. Start the frontend development server, which will run on port 3000.
3. Open your browser and navigate to `http://localhost:3000` to access the HealthMate application.
4. Register a new account or log in to start using the features.

## API Endpoints

The backend provides a comprehensive REST API. Here are the main endpoint categories:

- **User Management**: `/api/user/*` - Authentication, registration, profile management
- **Symptom Checker**: `/api/symptom_checker/predict` - Disease prediction from symptoms
- **Medication Reminders**: `/api/medication_reminder/*` - CRUD operations for reminders
- **Health Reports**: `/report/save`, `/api/user/medical_history/*` - Report generation and history
- **Report Analyzer**: `/api/reportanalyzer/analyze` - OCR and AI analysis of medical documents
- **Dashboard**: `/api/dashboard_charts/*` - Data for charts and analytics
- **Admin Panel**: `/admin/*` - Administrative functions including user controls, reports, and settings

## ML Model

The machine learning model is trained on a dataset of symptoms and corresponding diseases. It uses scikit-learn algorithms to predict potential diseases based on user-inputted symptoms. The model provides:

- Disease prediction with confidence scores
- Detailed descriptions, precautions, medications, diets, and workout recommendations
- Integration with master data files for comprehensive health information

Model files are located in `backend/Ai_model/` and training data in `backend/Training/`.

## Contributing

We welcome contributions to HealthMate! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code follows the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository or contact the development team.
