from datetime import timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from config import Config
from database.db import engine
from models.user_model import User
from models.disease_model import Disease
from models.diagnosis_model import Diagnosis
from routes.medicinereminder import medicinereminder_bp
from services.reminder_scheduler import start_scheduler

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Add secret key for session management
    app.secret_key = '466f37c4ffe5bd6ff846003771beb82d'  # Replace with a secure key in production

    # Configure session cookie for cross-origin requests in local dev
    app.config.update(
        SESSION_COOKIE_SAMESITE='Lax',
        SESSION_COOKIE_SECURE=False,  # Set True if using HTTPS
        PERMANENT_SESSION_LIFETIME=timedelta(minutes=30)  # Session timeout of 30 minutes
    )

    # --- Logging ---
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    app.config['DEBUG'] = True

    # --- CORS ---
    CORS(app, resources={
        r"/*": {
            "origins": "http://localhost:3000",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "Accept"],
            "supports_credentials": True,
            "expose_headers": ["Content-Type", "Authorization"]
        }
    })

    # --- Log all incoming requests ---
    @app.before_request
    def log_request_info():
        logging.debug(f"Incoming request: {request.method} {request.path}")
        logging.debug(f"Headers: {dict(request.headers)}")
        logging.debug(f"Body: {request.get_data()}")
        if request.method in ['POST', 'PUT']:
            content_type = request.headers.get('Content-Type', '')
            # Allow multipart/form-data for reportanalyzer analyze endpoint
            if request.path.startswith('/api/reportanalyzer/analyze') and 'multipart/form-data' in content_type:
                pass
            elif 'application/json' not in content_type:
                return jsonify({'error': 'Content-Type must be application/json'}), 415

    # --- Table Creation ---
    User.create_table()
    Disease.create_table()
    Diagnosis.create_table()

    # --- Route Blueprints ---
    from routes.symptom_checker import symptom_checker_bp
    from routes.user_routes import user_bp
    from routes.medicine_routes import medicine_bp
    from routes.health_report import report_bp
    from routes.profile import profile_bp
    from routes.medical_history_routes import medical_history_bp
    from routes.privacycontrol import privacycontrol_bp
    from routes.dashboard_charts import dashboard_charts_bp
    from routes.reportanalyzer import reportanalyzer_bp
    from routes.admin_user_management import admin_user_bp
    from routes.admin_health_reports import admin_health_reports_bp
    from routes.admin_analyzer_reports import admin_analyzer_reports_bp
    from routes.admin_auth import admin_auth_bp
    from routes.admin_dashboard import admin_dashboard_bp
    from routes.admin_disease_info import admin_disease_info_bp
    from routes.admin_user_controls import admin_user_controls_bp
    from routes.admin_system_logs import admin_system_logs_bp
    from routes.admin_feedback import admin_feedback_bp
    from routes.admin_settings import admin_settings_bp

    app.register_blueprint(symptom_checker_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(medicine_bp, url_prefix='/api/medicine')
    app.register_blueprint(report_bp, url_prefix='/report')  # Full: /report/save
    app.register_blueprint(profile_bp,url_prefix='/api/user/profile')
    app.register_blueprint(medical_history_bp,urlprefix='/api/user/medical_history')
    app.register_blueprint(privacycontrol_bp)
    app.register_blueprint(dashboard_charts_bp)
    app.register_blueprint(reportanalyzer_bp, url_prefix='/api/reportanalyzer')
    app.register_blueprint(admin_user_bp, url_prefix='/admin/users')
    app.register_blueprint(admin_health_reports_bp, url_prefix='/admin/health_reports')
    app.register_blueprint(admin_analyzer_reports_bp, url_prefix='/admin/analyzer_reports')
    app.register_blueprint(admin_auth_bp, url_prefix='/admin/auth')
    app.register_blueprint(admin_dashboard_bp, url_prefix='/admin/dashboard')
    app.register_blueprint(admin_disease_info_bp, url_prefix='/admin/disease_info')
    app.register_blueprint(admin_user_controls_bp, url_prefix='/admin/user_controls')
    app.register_blueprint(admin_system_logs_bp, url_prefix='/admin/system_logs')
    app.register_blueprint(admin_feedback_bp, url_prefix='/admin/feedback')
    app.register_blueprint(admin_settings_bp, url_prefix='/admin/settings')

    app.register_blueprint(medicinereminder_bp, url_prefix='/api/medicinereminder')

    # Start the reminder scheduler
    start_scheduler()

    return app

# --- CLI Entry Point ---
def create_cli_app():
    return create_app()

# --- Run ---
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
