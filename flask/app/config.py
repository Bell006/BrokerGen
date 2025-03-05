import os
import secrets

class Config:
    SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

class DevelopmentConfig(Config):
    # Development
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'brokergen.db')
    DEBUG = True 

class ProductionConfig(Config):
    # Production PostgreSQL (Neon)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")