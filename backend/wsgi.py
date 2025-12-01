import os
import sys


sys.path.insert(0, os.path.dirname(__file__))


def application(environ, start_response):
    from a2wsgi import ASGIMiddleware
    from app import create_app
    app = create_app()
    return ASGIMiddleware(app)(environ, start_response)
