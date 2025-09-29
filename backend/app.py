from datetime import timedelta
from flask import Flask, request, jsonify
from routes.medication_reminder_routes import medication_reminder_bp

from flask_cors import CORS
import logging
import os
from logging.handlers import RotatingFileHandler
from config import Config
from database.db import engine
from models.user_model import User
from models.disease_model import Disease
from models.diagnosis_model import Diagnosis


import threading
from services.notification_scheduler import start_scheduler

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    # Add secret key for session management
    app.secret_key = Config.SECRET_KEY

    # Configure session cookie for cross-origin requests in local dev
    app.config.update(
        SESSION_COOKIE_SAMESITE='Lax',
        SESSION_COOKIE_SECURE=False,  # Set True if using HTTPS
        PERMANENT_SESSION_LIFETIME=timedelta(minutes=30)  # Session timeout of 30 minutes
    )

    # --- Logging ---
    log_level = getattr(logging, Config.LOG_LEVEL)
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Add file handler for production logging
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/backend.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(log_level)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(log_level)
        app.logger.info('Backend startup')

    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', False)

    # --- CORS ---
    CORS(app, resources={
        r"/*": {
            "origins": Config.CORS_ORIGINS,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "Accept"],
            "supports_credentials": True,
            "expose_headers": ["Content-Type", "Authorization"]
        }
    })

    # --- Log all incoming requests ---
    @app.before_request
    def log_request_info():
        app.logger.info(f"Incoming request: {request.method} {request.path}")
        if request.method in ['POST', 'PUT']:
            content_type = request.headers.get('Content-Type', '')
            # Allow multipart/form-data for reportanalyzer analyze endpoint
            if request.path.startswith('/api/reportanalyzer/analyze') and 'multipart/form-data' in content_type:
                pass
            # Skip Content-Type check for deactivate, activate, and delete user endpoints to avoid 415 error
            elif request.path.startswith('/admin/users/deactivate') or request.path.startswith('/admin/users/activate') or request.path.startswith('/admin/users/delete'):
                pass
            elif 'application/json' not in content_type:
                return jsonify({'error': 'Content-Type must be application/json'}), 415

    # --- Handle 415 Unsupported Media Type errors globally ---
    @app.errorhandler(415)
    def handle_unsupported_media_type(error):
        return jsonify({'error': 'Unsupported Media Type'}), 415

    # --- Handle 500 Internal Server Error ---
    @app.errorhandler(500)
    def handle_internal_error(error):
        app.logger.error(f"Internal error: {str(error)}")
        return jsonify({'error': 'Internal server error'}), 500

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

    app.register_blueprint(medication_reminder_bp)
    app.register_blueprint(symptom_checker_bp)
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(medicine_bp, url_prefix='/api/medicine')
    app.register_blueprint(report_bp, url_prefix='/report')  # Full: /report/save
    app.register_blueprint(profile_bp, url_prefix='/api/user/profile')
    app.register_blueprint(medical_history_bp, url_prefix='/api/user/medical_history')
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

    # Start notification scheduler in background thread (conditionally)
    if not app.config.get('TESTING'):
        threading.Thread(target=start_scheduler, daemon=True).start()

    return app

# --- CLI Entry Point ---
def create_cli_app():
    return create_app()

# --- Run ---
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
