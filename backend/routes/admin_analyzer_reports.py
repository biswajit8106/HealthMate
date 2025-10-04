from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from utils.auth import get_current_admin
import os

router = APIRouter()

# Assuming there is a model or database table for analyzer uploads, here we simulate with file system

UPLOAD_FOLDER = 'backend/static/analyzer_uploads'

@router.get('/')
def list_uploads(admin_id: int = Depends(get_current_admin)):
    try:
        files = os.listdir(UPLOAD_FOLDER)
        uploads = []
        for filename in files:
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                uploads.append({
                    'filename': filename,
                    'size': os.path.getsize(filepath),
                    'path': filepath
                })
        return uploads
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/download/{filename}')
def download_upload(filename: str, admin_id: int = Depends(get_current_admin)):
    try:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail='File not found')
        return FileResponse(path=filepath, filename=filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete('/delete/{filename}')
def delete_upload(filename: str, admin_id: int = Depends(get_current_admin)):
    try:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail='File not found')
        os.remove(filepath)
        return {'message': 'File deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
