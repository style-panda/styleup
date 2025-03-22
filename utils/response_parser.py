import json
import logging
from collections import OrderedDict

logger = logging.getLogger(__name__)

# Define the desired order of keys based on the prompt
KEY_ORDER = [
    "body_shape_and_physical_attributes",
    "skin_tone_and_hair_color",
    "age_and_gender",
    "personal_style_and_preferences",
    "accessories_and_jewelry",
    "context_of_the_photos",
    "cultural_or_regional_influences",
    "facial_features_and_expressions",
    "color_preferences_and_palette",
    "fit_and_silhouette_preferences",
    "footwear_choices",
    "grooming_and_personal_care",
    "lifestyle_indicators",
    "seasonal_and_climate_considerations",
    "confidence_and_body_language",
    "summary",
    "notes"
]

def parse_json_response(raw_text):
    """
    Parse the raw text response from Gemini into a structured JSON object
    with keys in the specified order.
    
    Args:
        raw_text (str): The raw text response from Gemini
        
    Returns:
        tuple: (parsed_json, error_message)
    """
    try:
        logger.info("Parsing raw text response")
        
        # Extract JSON from the text (in case there's additional text)
        json_start = raw_text.find('{')
        json_end = raw_text.rfind('}') + 1
        
        if json_start == -1 or json_end == 0:
            logger.error("No JSON found in response")
            return None, "No JSON found in response"
        
        json_str = raw_text[json_start:json_end]
        
        # Parse the JSON
        parsed_json = json.loads(json_str)
        logger.info("Successfully parsed JSON response")
        
        # Reorder the keys according to the defined order
        ordered_json = OrderedDict()
        
        # Add keys in the specified order
        for key in KEY_ORDER:
            if key in parsed_json:
                ordered_json[key] = parsed_json[key]
        
        # Add any remaining keys that weren't in our predefined order
        for key in parsed_json:
            if key not in ordered_json:
                ordered_json[key] = parsed_json[key]
        
        logger.info("Successfully reordered JSON keys")
        return ordered_json, None
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {str(e)}")
        return None, f"Invalid JSON format: {str(e)}"
    except Exception as e:
        logger.error(f"Error parsing response: {str(e)}")
        return None, f"Error parsing response: {str(e)}"