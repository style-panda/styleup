
from routes.analysis import analysis_bp
from routes.suggestions import suggestions_bp

def register_routes(app):
    """Register all blueprints/routes with the app."""
    app.register_blueprint(analysis_bp)
    app.register_blueprint(suggestions_bp)