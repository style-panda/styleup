from flask import Blueprint, jsonify, request
from services import image_service, gemini_service
from utils import response_parser
import json
from collections import OrderedDict


analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/api/analyze-images', methods=['POST'])
def analyze_images():
    """
    Process and analyze images using the Gemini API.
    
    Accepts images as URLs in the request. Each image in the 'images' array
    should be an object with 'url' and optional 'mime_type'.
    
    Example request:
    {
        "images": [
            {"url": "https://example.com/image1.jpg"},
            {"url": "https://example.com/image2.png", "mime_type": "image/png"}
        ]
    }
    
    Returns:
        JSON response with analysis results or error message
    """

    uploaded_images = request.json.get('images') if request.is_json else None
    

    image_parts, error = image_service.load_images(uploaded_images)
    if error:
        return jsonify({"error": error}), 400


    raw_text, error = gemini_service.analyze_with_gemini(image_parts)
    if error:
        return jsonify({"error": f"Gemini API error: {error}"}), 500
    

    result, error = response_parser.parse_json_response(raw_text)
    if error:
        return jsonify({"error": f"Failed to parse JSON: {error}"}), 500
    
    class OrderedEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, OrderedDict):
                return dict(obj)
            return super().default(obj)
    
    return json.dumps(result, cls=OrderedEncoder), 200, {'Content-Type': 'application/json'}