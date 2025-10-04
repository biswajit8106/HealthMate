import os
import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from database.db import get_db
from models.user_model import User
from models.health_report_model import HealthReport
from utils.auth import get_current_admin

router = APIRouter()

@router.get('/stats')
def get_stats(admin_id: int = Depends(get_current_admin), db: Session = Depends(get_db)):
    try:
        total_users = db.query(func.count(User.user_id)).scalar()
        total_reports = db.query(func.count(HealthReport.id)).scalar()
        analyzer_uploads_folder = 'backend/static/analyzer_uploads'
        total_analyzer_uploads = 0
        if os.path.exists(analyzer_uploads_folder) and os.path.isdir(analyzer_uploads_folder):
            total_analyzer_uploads = len([f for f in os.listdir(analyzer_uploads_folder) if os.path.isfile(os.path.join(analyzer_uploads_folder, f))])
        return {
            'total_users': total_users,
            'total_reports': total_reports,
            'total_analyzer_uploads': total_analyzer_uploads
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/user_growth')
def user_growth(admin_id: int = Depends(get_current_admin), db: Session = Depends(get_db)):
    try:
        results = db.query(
            extract('year', User.created_at).label('year'),
            extract('month', User.created_at).label('month'),
            func.count(User.user_id)
        ).group_by('year', 'month').order_by('year', 'month').all()
        data = [{'year': r[0], 'month': r[1], 'count': r[2]} for r in results]
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/symptom_check_usage')
def symptom_check_usage(admin_id: int = Depends(get_current_admin), db: Session = Depends(get_db)):
    try:
        results = db.query(
            func.date(HealthReport.created_at),
            func.count(HealthReport.id)
        ).group_by(func.date(HealthReport.created_at)).order_by(func.date(HealthReport.created_at)).all()
        data = [{'date': r[0].isoformat(), 'count': r[1]} for r in results]
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/report_analyzer_trends')
def report_analyzer_trends(admin_id: int = Depends(get_current_admin)):
    try:
        analyzer_uploads_folder = 'backend/static/analyzer_uploads'
        date_counts = {}
        if os.path.exists(analyzer_uploads_folder) and os.path.isdir(analyzer_uploads_folder):
            files = os.listdir(analyzer_uploads_folder)
            for f in files:
                path = os.path.join(analyzer_uploads_folder, f)
                if os.path.isfile(path):
                    mod_time = os.path.getmtime(path)
                    date_str = datetime.datetime.fromtimestamp(mod_time).date().isoformat()
                    date_counts[date_str] = date_counts.get(date_str, 0) + 1
        data = [{'date': k, 'count': v} for k, v in sorted(date_counts.items())]
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/recent_activity')
def recent_activity(admin_id: int = Depends(get_current_admin), db: Session = Depends(get_db)):
    try:
        recent_users = db.query(User).order_by(User.created_at.desc()).limit(10).all()
        recent_reports = db.query(HealthReport).order_by(HealthReport.created_at.desc()).limit(10).all()
        users_data = [{
            'type': 'user_registration',
            'user_id': u.user_id,
            'name': u.name,
            'created_at': u.created_at.isoformat() if u.created_at else None
        } for u in recent_users]
        reports_data = [{
            'type': 'report_generated',
            'report_id': r.id,
            'user_id': r.user_id,
            'predicted_disease': r.predicted_disease,
            'created_at': r.created_at.isoformat() if r.created_at else None
        } for r in recent_reports]
        combined = users_data + reports_data
        combined_sorted = sorted(combined, key=lambda x: x['created_at'] or '', reverse=True)
        return combined_sorted[:10]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
