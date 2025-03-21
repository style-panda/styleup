import os
import logging
import google.generativeai as genai

def configure_app(app):
    """Configure the application with necessary settings."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize Google Gemini client
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
        
    genai.configure(api_key=api_key)
    
    # Add any additional configuration here
    app.config['JSON_SORT_KEYS'] = False