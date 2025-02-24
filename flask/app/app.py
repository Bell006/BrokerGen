from flask import Flask, jsonify
from app.app_error import AppError 
from flask_cors import CORS
from app.config import Config
from dotenv import load_dotenv
import os
from database import db, init_db
from app.routes.auth_routes import auth_bp
from app.routes.image_routes import image_bp

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    @app.errorhandler(AppError)
    def handle_app_error(error):
        response = jsonify({'message': str(error)})
        response.status_code = error.status_code
        return response

    CORS(app, 
        resources={r"/api/*": {
            "origins": ["https://buriticorretores.netlify.app", "http://localhost:5173"],
            "allow_headers": ["Content-Type", "Authorization"],
            "methods": ["GET", "POST", "OPTIONS"]
        }}
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