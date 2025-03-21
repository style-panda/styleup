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
    # Get the path from the request
    path = context.req.path or "/"
    
    # Create a mock body content based on the request type
    if isinstance(context.req.body, dict):
        # If body is already parsed as JSON dict
        body_content = json.dumps(context.req.body).encode('utf-8')
        # Make sure Content-Type reflects this
        if 'content-type' not in context.req.headers:
            context.req.headers['content-type'] = 'application/json'
    elif context.req.body:
        # If body exists but is not a dict
        body_content = context.req.body
    else:
        # Empty body
        body_content = b''
    
    # Create a stream-like object for the WSGI environment
    class BodyStream:
        def __init__(self, content):
            self.content = content
            self.position = 0
        
        def read(self, size=None):
            if size is None:
                result = self.content[self.position:]
                self.position = len(self.content)
            else:
                result = self.content[self.position:self.position + size]
                self.position += size
            return result
    
    body_stream = BodyStream(body_content)
    
    # Set up the WSGI environment
    environ = {
        'wsgi.input': body_stream,
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
        'CONTENT_LENGTH': str(len(body_content)),
        'SERVER_NAME': 'appwrite-function',
        'SERVER_PORT': '443',
        'SERVER_PROTOCOL': 'HTTP/1.1',
    }
    
    # Add HTTP headers
    for key, value in context.req.headers.items():
        key = key.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            environ[f'HTTP_{key}'] = value
    
    # Storage for response data
    response_data = []
    response_headers = [('Content-Type', 'text/html')]
    response_status = '200 OK'
    
    # Define a function to capture the response
    def start_response(status, headers):
        nonlocal response_status, response_headers
        response_status = status
        response_headers = headers
    
    try:
        # Process the request through Flask
        for data in app(environ, start_response):
            if isinstance(data, str):
                data = data.encode('utf-8')
            response_data.append(data)
        
        # Combine all response chunks
        body = b''.join(response_data)
        
        # Get the status code as an integer
        status_code = int(response_status.split(' ')[0])
        
        # Check content type to determine response format
        content_type = dict(response_headers).get('Content-Type', '')
        
        if content_type.startswith('application/json'):
            try:
                # For JSON responses
                return context.res.json(json.loads(body.decode('utf-8')))
            except:
                # Fallback to text
                return context.res.text(body.decode('utf-8'))
        elif content_type.startswith('text/'):
            # For text responses
            return context.res.text(body.decode('utf-8'))
        else:
            # For binary responses
            return context.res.binary(body)
    
    except Exception as e:
        # Log the exception
        context.error(f"Exception in Flask app: {str(e)}")
        
        # Return an error response
        return context.res.json({
            "error": "Internal Server Error",
            "message": str(e)
        }, 500)