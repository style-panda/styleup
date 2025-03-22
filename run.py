import os
import sys

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

if __name__ == "__main__":
    # Set debug environment variable
    os.environ['FLASK_DEBUG'] = '1'
    
    # Import and run the app directly
    from src.main import app
    app.run(debug=True)