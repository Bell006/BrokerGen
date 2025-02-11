from flask import Blueprint, request, jsonify
from app.models import Broker
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    creci = data.get('creci')

    broker = Broker.query.filter_by(email=email, creci=creci).first()

    if broker:
        return jsonify({
            'message': 'Login successful', 
            'broker': broker.to_dict()
        }), 200
    else:
        return jsonify({
            'message': 'Credenciais inválidas.'
        }), 401