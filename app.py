from flask import Flask, request, jsonify
import os
import base64
import json
import re
import google.generativeai as genai
from flask_cors import CORS
from .config import configure_app
from routes import register_routes

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    
    # Configure the application
    configure_app(app)
    
    # Register all routes
    register_routes(app)
    
    return app

app = create_app()

# For local development
if __name__ == '__main__':
    app.run(debug=True)

# For Appwrite Functions
def main(req, res):
    # Get the path from the request
    path = req.path or "/"
    
    # Set up the WSGI environment
    environ = {
        'wsgi.input': req.body,
        'wsgi.errors': None,
        'wsgi.version': (1, 0),
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
        'wsgi.url_scheme': 'https',
        'REQUEST_METHOD': req.method,
        'PATH_INFO': path,
        'QUERY_STRING': req.query_string or "",
        'CONTENT_TYPE': req.headers.get('content-type', ''),
        'CONTENT_LENGTH': req.headers.get('content-length', ''),
        'SERVER_NAME': 'appwrite-function',
        'SERVER_PORT': '443',
        'SERVER_PROTOCOL': 'HTTP/1.1',
    }
    
    # Add HTTP headers
    for key, value in req.headers.items():
        key = key.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            environ[f'HTTP_{key}'] = value
    
    # Define a function to capture the response
    def start_response(status, headers):
        res.status = int(status.split(' ')[0])
        for header, value in headers:
            res.headers[header] = value
    
    # Process the request through Flask
    response_data = b''
    for data in app(environ, start_response):
        if isinstance(data, str):
            data = data.encode('utf-8')
        response_data += data
    
    res.body = response_data
    return res