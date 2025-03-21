from flask import Blueprint, jsonify, request
from services import image_service, gemini_service 
from utils import response_parser


analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/api/analyze-images', methods=['POST'])
def analyze_images():
    """
    Process and analyze images using the Gemini API.
    
    Accepts images either uploaded in the request or uses default images
    from local paths if none are provided. Returns structured analysis results.
    
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
    
    # Parse the response
    result, error = response_parser.parse_json_response(raw_text)
    if error:
        return jsonify({"error": f"Failed to parse JSON: {error}"}), 500
    
    return jsonify(result)