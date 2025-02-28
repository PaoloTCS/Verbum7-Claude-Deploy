# /Users/paolopignatelli/VerbumTechnologies/Verbum7-Claude/backend/app/__init__.py
"""
app/__init__.py
Application factory for Semantic Tiles.
"""

import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

def create_app(env):
    """Create and configure the Flask application."""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    # Allow all origins in production, or use environment variable
    origins = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000').split(',')
    CORS(app, resources={r"/*": {"origins": origins}})
    
    # Configuration
    app.config.update(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev-key-change-in-production'),
        UPLOAD_FOLDER=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads'),
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max file size
        TEMPLATES_AUTO_RELOAD=True if env == 'development' else False
    )
    
    # Import and register blueprints
    from app.api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Default route
    @app.route('/')
    def index():
        return app.send_static_file('index.html')
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    return app