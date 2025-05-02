from functools import wraps
from flask import request, jsonify
import jwt
import os
from app.models import Broker

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            current_broker = Broker.query.get(data['broker_id'])
        except:
            return jsonify({'message': 'Invalid token'}), 401

        return f(current_broker, *args, **kwargs)
    
    return decorated