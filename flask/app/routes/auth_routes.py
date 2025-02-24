from flask import Blueprint, request, jsonify
from flask_wtf.csrf import generate_csrf
from flask import make_response
from app.models import Broker
from database import db
from dotenv import load_dotenv
import os

from app.utils.utils_google_api import GoogleAPI
from app.utils.utils_format import UserInputValidator
from app.app_error import AppError

load_dotenv()

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/csrf-token', methods=['GET'])
def get_csrf():
    token = generate_csrf()
    response = make_response(jsonify({'csrf_token': token}))
    response.set_cookie('csrf_token', 
                       token,
                       samesite='None', 
                       secure=True,      
                       httponly=True)
    
    return response

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    uau = data.get('code_uau')

    if not email or not uau:
        raise AppError('Email e código UAU são obrigatórios.', 400)

    broker = Broker.query.filter_by(email=email, uau=uau).first()

    if not broker:
            raise AppError('Credenciais inválidas.', 401)
    
    return jsonify({'message': 'Login successful', 'broker': broker.to_dict()}), 200

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    
    required_fields = ['name', 'email', 'code_uau']
    for field in required_fields:
        if not data.get(field):
            raise AppError(f'Campo {field} é obrigatório.', 400)
    
    name = data.get('name')
    email = data.get('email')
    uau = data.get('code_uau')

    UserInputValidator.validate_name(name)

    try:
        google_api = GoogleAPI() # Initialize Google API client
        gc = google_api.get_google_sheets_service()

        spreadsheet_id = os.getenv('GOOGLE_SHEET_UAU_ID')
        sh = gc.open_by_key(spreadsheet_id)

        worksheet = sh.sheet1

        uau_codes = worksheet.col_values(1)

    except Exception as e:
        raise AppError(f'Erro ao acessar a planilha do Google Sheets: {str(e)}', 500)
    
    if uau not in uau_codes:
        raise AppError('Código UAU inválido.', 400)
    
    existing_broker = Broker.query.filter(
        (Broker.email == email) | (Broker.uau == uau)
    ).first()
    
    if existing_broker:
        raise AppError('Corretor já cadastrado com este email ou código UAU.', 400)
    
        # Create new broker
    new_broker = Broker(
        name=name,
        email=email,
        uau=uau,
        is_admin=False
    )

    try:
        db.session.add(new_broker)
        db.session.commit()
        
        return jsonify({'message': 'Cadastro realizado com sucesso.', 'broker': new_broker.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        raise AppError(f'Erro ao cadastrar corretor: {str(e)}', 500)