from flask import Flask, request, jsonify
import os
import base64
import json
import re
import google.generativeai as genai
from flask_cors import CORS
from appwrite.client import Client
from appwrite.services.users import Users
from appwrite.exception import AppwriteException

from .config import configure_app
from ..routes import register

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    
    # Configure the application
    configure_app(app)
    
    # Register all routes
    register.register_routes(app)
    
    return app

app = create_app()

# For local development
if __name__ == '__main__':
    app.run(debug=True)

# For Appwrite Functions
def main(context):
    """
    Main entry point for Appwrite Functions.
    This function processes the request through the Flask app.
    """
    # Get the path from the request
    path = context.req.path or "/"
    
    # Set up the WSGI environment
    environ = {
        'wsgi.input': context.req.body,
        'wsgi.errors': None,
        'wsgi.version': (1, 0),
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
        'wsgi.url_scheme': 'https',
        'REQUEST_METHOD': context.req.method,
        'PATH_INFO': path,
        'QUERY_STRING': context.req.query_string or "",
        'CONTENT_TYPE': context.req.headers.get('content-type', ''),
        'CONTENT_LENGTH': context.req.headers.get('content-length', ''),
        'SERVER_NAME': 'appwrite-function',
        'SERVER_PORT': '443',
        'SERVER_PROTOCOL': 'HTTP/1.1',
    }
    
    # Add HTTP headers
    for key, value in context.req.headers.items():
        key = key.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            environ[f'HTTP_{key}'] = value
    
    # Dict to capture the response
    response_info = {
        'status': 200,
        'headers': [],
        'body': b''
    }
    
    # Define a function to capture the response
    def start_response(status, headers):
        response_info['status'] = int(status.split(' ')[0])
        response_info['headers'] = headers
    
    # Process the request through Flask
    for data in app(environ, start_response):
        if isinstance(data, str):
            data = data.encode('utf-8')
        response_info['body'] += data
    
    # Set the status code
    context.res.status = response_info['status']
    
    # Set headers using context.res methods
    for header, value in response_info['headers']:
        # Use set_header method instead of accessing headers dict
        context.res.set_header(header, value)
    
    # Return the appropriate response object
    if response_info['headers'] and dict(response_info['headers']).get('Content-Type', '').startswith('application/json'):
        # For JSON responses
        try:
            return context.res.json(json.loads(response_info['body']))
        except:
            # Fall back to raw text if JSON parsing fails
            return context.res.send(response_info['body'], response_info['status'])
    else:
        # For other content types
        return context.res.send(response_info['body'], response_info['status'])