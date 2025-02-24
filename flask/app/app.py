from flask import Flask, jsonify
from app.app_error import AppError 
from flask_cors import CORS
from app.config import Config
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os
from database import db, init_db
from app.routes.auth_routes import auth_bp
from app.routes.image_routes import image_bp

load_dotenv()

def create_app():
    
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.errorhandler(AppError)
    def handle_app_error(error):
        response = jsonify({'message': str(error)})
        response.status_code = error.status_code
        return response

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    csrf = CSRFProtect(app)

    CORS(app, 
        resources={r"/api/*": {
            "origins": ["http://localhost:5173", "https://buriticorretores.netlify.app"],
            "supports_credentials": True,
            "expose_headers": ["x-csrftoken", "X-CSRFToken"],
            "allow_headers": ["Content-Type", "x-csrftoken", "X-CSRFToken"]
        }},
        supports_credentials=True
    )

    # Initialize database
    db.init_app(app)
    init_db(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(image_bp, url_prefix='/api')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=False)