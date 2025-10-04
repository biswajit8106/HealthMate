from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database.db import get_db
from models.health_report_model import HealthReport
from utils.auth import get_current_admin
from typing import Optional
import os

router = APIRouter()

@router.get('/')
def list_reports(
    admin_id: int = Depends(get_current_admin),
    db: Session = Depends(get_db),
    user_id: Optional[int] = Query(None),
    disease: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None)
):
    try:
        query = db.query(HealthReport)

        if user_id:
            query = query.filter(HealthReport.user_id == user_id)
        if disease:
            query = query.filter(HealthReport.predicted_disease.ilike(f"%{disease}%"))
        if start_date:
            query = query.filter(HealthReport.created_at >= start_date)
        if end_date:
            query = query.filter(HealthReport.created_at <= end_date)

        reports = query.all()

        reports_data = []
        for report in reports:
            reports_data.append({
                'id': report.id,
                'user_id': report.user_id,
                'name': report.name,
                'gender': report.gender,
                'age': report.age,
                'predicted_disease': report.predicted_disease,
                'confidence': report.confidence,
                'description': report.description,
                'created_at': report.created_at.isoformat()
            })
        return reports_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/download/{report_id}')
def download_report(report_id: int, admin_id: int = Depends(get_current_admin)):
    try:
        # Assuming reports are saved as PDFs in a directory with filename pattern report_<id>.pdf
        report_path = f'backend/static/reports/report_{report_id}.pdf'
        if not os.path.exists(report_path):
            raise HTTPException(status_code=404, detail='Report file not found')
        return FileResponse(path=report_path, filename=f'report_{report_id}.pdf', media_type='application/pdf')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete('/delete/{report_id}')
def delete_report(report_id: int, admin_id: int = Depends(get_current_admin), db: Session = Depends(get_db)):
    try:
        report = db.query(HealthReport).filter(HealthReport.id == report_id).first()
        if not report:
            raise HTTPException(status_code=404, detail='Report not found')
        # Soft delete or archive logic can be implemented here
        db.delete(report)
        db.commit()
        return {'message': 'Report deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
