from flask import Flask, request, jsonify
import os
import base64
import json
import re
import google.generativeai as genai
from flask_cors import CORS
from prompts import image_analysis_prompt, form_and_user_analysis_to_suggestions_prompt
from local_constants import image_paths
from config import configure_app
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

if __name__ == '__main__':
    app.run(debug=True)