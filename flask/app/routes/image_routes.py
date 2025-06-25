from flask import Blueprint, request, jsonify
from app.tasks import generate_image_task
from celery.result import AsyncResult
from app.tasks import celery_app

from app.utils.auth import token_required
from app.app_error import AppError

image_bp = Blueprint('image', __name__)
@image_bp.errorhandler(AppError)

# Rota de criação da imagem 
@image_bp.route('/create_image', methods=['POST'])
@token_required
def create_broker_images(current_broker):
    data = request.get_json()
    task = generate_image_task.delay(data)

    return jsonify({
        'message': 'Imagem em processamento',
        'task_id': task.id
    }), 202


# Rota de status (consultar o resultado da task)
@image_bp.route('/task_status/<task_id>', methods=['GET'])
def get_task_status(task_id):
    task = celery_app.AsyncResult(task_id)

    if task.state == 'PENDING':
        return jsonify({
            'state': task.state,
            'result': {
                'generated_images': [],
                'progress': 0,
                'total': 1  # evita divisão por zero
            }
        })

    elif task.state == 'STARTED':
        return jsonify({
            'state': task.state,
            'result': task.info  
        })

    elif task.state == 'SUCCESS':
        return jsonify({
            'state': task.state,
            'result': task.result
        })

    elif task.state == 'FAILURE':
        return jsonify({
            'state': 'FAILURE',
            'error': str(task.result) 
        }), 500

    return jsonify({'state': task.state})