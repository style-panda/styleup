import json
import re
import logging

logger = logging.getLogger(__name__)

def parse_json_response(raw_text):
    """Parse JSON from Gemini API response."""
    try:
        # Check if the response contains a JSON code block
        if "```json" in raw_text and "```" in raw_text:
            # Extract the JSON string between the code block markers
            json_match = re.search(r'```json\s*([\s\S]*?)\s*```', raw_text)
            if json_match:
                json_string = json_match.group(1).strip()
                parsed_json = json.loads(json_string)
                return parsed_json, None
        
        # If no JSON code block is found or extraction failed, try to parse the entire text
        try:
            parsed_json = json.loads(raw_text)
            return parsed_json, None
        except json.JSONDecodeError:
            # If all parsing attempts fail, return the raw text
            return {"analysis": raw_text}, None
            
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {str(e)}")
        return None, str(e)
    except Exception as e:
        logger.error(f"Error parsing response: {str(e)}")
        return None, str(e)