import json
import logging
import google.generativeai as genai

from .prompts import image_analysis_prompt, form_and_user_analysis_to_suggestions_prompt


logger = logging.getLogger(__name__)

def analyze_with_gemini(image_parts):
    """Analyze images with Gemini API."""
    try:
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-2.0-flash-001')
        
        # Create the response
        response = model.generate_content([image_analysis_prompt, *image_parts])
        
        return response.text, None
    except Exception as e:
        logger.error(f"Error in Gemini analysis: {str(e)}")
        return None, str(e)

def get_suggestions(form_data, image_analysis):
    """Get fashion suggestions from Gemini."""
    try:
        # Prepare the input for Gemini
        input_data = {
            "client_form": form_data,
            "client_analysis": image_analysis
        }
        
        # Convert to JSON string
        input_json = json.dumps(input_data)
        
        # Create the Gemini model
        model = genai.GenerativeModel('gemini-2.0-flash-001')
        
        # Generate fashion suggestions
        response = model.generate_content(
            [form_and_user_analysis_to_suggestions_prompt, input_json]
        )
        
        return response.text, None
    except Exception as e:
        logger.error(f"Error getting suggestions: {str(e)}")
        return None, str(e)