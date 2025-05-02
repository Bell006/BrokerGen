from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from app.app_error import AppError
from app.config import DevelopmentConfig, ProductionConfig
from database import init_db
from app.routes.auth_routes import auth_bp
from app.routes.image_routes import image_bp

def create_app():
    load_dotenv()
    ENV = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)

    if ENV == "production":
        app.config.from_object(ProductionConfig)
        cors_origins = os.getenv("CORS_ORIGINS_PROD")
    else:
        app.config.from_object(DevelopmentConfig)
        cors_origins = os.getenv("CORS_ORIGINS_DEV")

    CORS(app, 
        resources={r"/api/*": {
            "origins": cors_origins,
            "allow_headers": ["Content-Type", "Authorization"],
            "methods": ["GET", "POST", "OPTIONS"]
        }}
    )

    @app.errorhandler(AppError)
    def handle_app_error(error):
        return jsonify({'message': str(error)}), error.status_code

    init_db(app)

    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(image_bp, url_prefix='/api')

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=(os.getenv("FLASK_ENV", "development") == "development"))
