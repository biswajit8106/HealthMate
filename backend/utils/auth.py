from fastapi import HTTPException, Request

# For simplicity, using cookies for session-like behavior
# In production, consider JWT tokens

def get_current_user(request: Request):
    user_id = request.cookies.get('user_id')
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    return int(user_id)

def get_current_admin(request: Request):
    admin_user_id = request.cookies.get('admin_user_id')
    if not admin_user_id:
        raise HTTPException(status_code=401, detail="Admin authentication required")
    return int(admin_user_id)
