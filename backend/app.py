from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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

# Import routers
from routes.medication_reminder_routes import router as medication_reminder_router
from routes.symptom_checker import router as symptom_checker_router
from routes.user_routes import router as user_router
from routes.medicine_routes import router as medicine_router
from routes.health_report import router as report_router
from routes.profile import router as profile_router
from routes.medical_history_routes import router as medical_history_router
from routes.privacycontrol import router as privacycontrol_router
from routes.dashboard_charts import router as dashboard_charts_router
from routes.reportanalyzer import router as reportanalyzer_router
from routes.admin_user_management import router as admin_user_router
from routes.admin_health_reports import router as admin_health_reports_router
from routes.admin_analyzer_reports import router as admin_analyzer_reports_router
from routes.admin_auth import router as admin_auth_router
from routes.admin_dashboard import router as admin_dashboard_router
from routes.admin_disease_info import router as admin_disease_info_router
from routes.admin_user_controls import router as admin_user_controls_router
from routes.admin_system_logs import router as admin_system_logs_router
from routes.admin_feedback import router as admin_feedback_router
from routes.admin_settings import router as admin_settings_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    # Table Creation
    User.create_table()
    Disease.create_table()
    Diagnosis.create_table()

    # Start notification scheduler in background thread
    if not os.getenv('TESTING'):
        threading.Thread(target=start_scheduler, daemon=True).start()

    yield
    # Shutdown
    # Add any cleanup here if needed

def create_app():
    app = FastAPI(
        title="HealthMate API",
        description="A comprehensive health management API",
        version="1.0.0",
        lifespan=lifespan
    )

    # --- Logging ---
    log_level = getattr(logging, Config.LOG_LEVEL)
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Add file handler for production logging
    if not os.getenv('FLASK_DEBUG', False):
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/backend.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(log_level)
        logging.getLogger().addHandler(file_handler)

    # --- CORS ---
    app.add_middleware(
        CORSMiddleware,
        allow_origins=Config.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "Accept"],
    )

    # --- Middleware for normalizing path ---
    @app.middleware("http")
    async def normalize_path(request: Request, call_next):
        path = request.scope['path']
        if path.startswith('//'):
            request.scope['path'] = '/' + path.lstrip('/')
        response = await call_next(request)
        return response

    # --- Middleware for logging requests ---
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        logging.info(f"Incoming request: {request.method} {request.url.path}")
        response = await call_next(request)
        return response

    # --- Exception Handlers ---
    @app.exception_handler(500)
    async def internal_error_handler(request: Request, exc: Exception):
        logging.error(f"Internal error: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )

    # --- Root Route ---
    @app.get("/")
    async def index():
        return {"message": "HealthMate backend is live"}

    # --- Include Routers ---
    app.include_router(medication_reminder_router)
    app.include_router(symptom_checker_router)
    app.include_router(user_router, prefix="/api/user")
    app.include_router(medicine_router, prefix="/api/medicine")
    app.include_router(report_router, prefix="/report")
    app.include_router(profile_router, prefix="/api/user/profile")
    app.include_router(medical_history_router, prefix="/api/user/medical_history")
    app.include_router(privacycontrol_router)
    app.include_router(dashboard_charts_router, prefix="/report/dashboard")
    app.include_router(reportanalyzer_router, prefix="/api/reportanalyzer")
    app.include_router(admin_user_router, prefix="/admin/users")
    app.include_router(admin_health_reports_router, prefix="/admin/health_reports")
    app.include_router(admin_analyzer_reports_router, prefix="/admin/analyzer_reports")
    app.include_router(admin_auth_router, prefix="/admin/auth")
    app.include_router(admin_dashboard_router, prefix="/admin/dashboard")
    app.include_router(admin_disease_info_router, prefix="/admin/disease_info")
    app.include_router(admin_user_controls_router, prefix="/admin/user_controls")
    app.include_router(admin_system_logs_router, prefix="/admin/system_logs")
    app.include_router(admin_feedback_router, prefix="/admin/feedback")
    app.include_router(admin_settings_router, prefix="/admin/settings")

    return app

# --- CLI Entry Point ---
def create_cli_app():
    return create_app()

# --- Run ---
if __name__ == '__main__':
    import uvicorn
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)
