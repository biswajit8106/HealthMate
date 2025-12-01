# TODO: Make Backend Production Ready for cPanel Hosting

- [x] Add 'a2wsgi' to backend/requirements.txt for ASGI to WSGI conversion
- [x] Create backend/wsgi.py file to wrap FastAPI app with ASGIMiddleware for WSGI callable
- [x] Modify backend/app.py to disable reload in production mode (check PRODUCTION env var)
- [x] Verify config.py is production-ready (uses env vars)
- [x] Update root route message to "HealthMate backend running"
- [ ] Test changes locally if possible
- [ ] Deploy to cPanel and set environment variables (DATABASE_URL, SECRET_KEY, etc.)
