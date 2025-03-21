from flask import Blueprint, jsonify, request
from ..services import gemini_service
from ..utils import response_parser

suggestions_bp = Blueprint('suggestions', __name__)

@suggestions_bp.route('/api/get_fashion_suggestions', methods=['POST'])
def get_fashion_suggestions():
    """Generate fashion suggestions based on form data and image analysis."""

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
        

    form_data = request.json.get('formData')
    

    image_analysis = request.json.get('imageAnalysis')
    
    if not form_data or not image_analysis:
        return jsonify({"error": "Both formData and imageAnalysis are required"}), 400
    

    suggestions_text, error = gemini_service.get_suggestions(form_data, image_analysis)
    if error:
        return jsonify({"error": f"Gemini API error: {error}"}), 403
    

    suggestions_json, error = response_parser.parse_json_response(suggestions_text)
    if error:
        return jsonify({
            "error": "Failed to parse suggestions as JSON", 
            "raw_response": suggestions_text
        }), 500
    
    return jsonify({"suggestions": suggestions_json})