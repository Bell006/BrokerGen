from functools import wraps
from flask import request, jsonify
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
import os
from app.models import Broker

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == 'OPTIONS':
            return '', 200

        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token indisponível.'}), 401

        try:
            token = token.split(' ')[1]  # Remove 'Bearer '
            payload = jwt.decode(
                token,
                os.getenv('SECRET_KEY'),
                algorithms=['HS256']
            )
            current_broker = Broker.query.get(payload['broker_id'])

            if not current_broker:
                return jsonify({'message': 'Corretor não encontrado.'}), 404

        except ExpiredSignatureError:
            return jsonify({'message': 'Sessão expirada. Faça login novamente.'}), 401
        except InvalidTokenError:
            return jsonify({'message': 'Token inválido.'}), 401
        except Exception as e:
            print(f"Erro interno no token_required: {e}")
            return jsonify({'message': 'Erro ao validar o token.'}), 500

        return f(current_broker, *args, **kwargs)

    return decorated
