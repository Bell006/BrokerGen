from flask import Blueprint, request, jsonify
import os
from flask import request, jsonify
from dotenv import load_dotenv

from app.utils.auth import token_required
from app.utils.utils_files import FileManager
from app.utils.utils_format import UserInputValidator
from app.utils.utils_google_api import GoogleAPI
from app.app_error import AppError

load_dotenv()
google_drive_template_folder_id = os.getenv('GOOGLE_DRIVE_TEMPLATE_FOLDER_ID')
google_api = GoogleAPI()
fileManager = FileManager()

image_bp = Blueprint('image', __name__)
@image_bp.errorhandler(AppError)

@image_bp.route('/create_image', methods=['POST'])

@token_required
def create_broker_images(current_broker):
    try:
        data = request.get_json()

        phone = data.get('phone', '')
        name = data.get('name', '').upper()
        creci = data.get('creci', '')
        categories = data.get('categories', [])

        if not name or not phone or not creci:
           raise AppError('Preencha todos os campos.', 400)
        
        if len(creci) < 4 or len(creci) > 5 or not creci.isdigit():
            raise AppError('Insira um código CRECI válido (4 a 5 dígitos numéricos).', 400)
        
        # Format the phone number
        formatted_phone = UserInputValidator.format_phone_number(phone)

        # Validates name
        UserInputValidator.validate_name(name)
        
        box_position_feed_general = (150, 1025)
        box_position_stories_general = (312, 1615)

        box_position_stories_condicoes = (120, 1560)
        box_position_feed_condicoes1 = (718, 955)
        box_position_feed_condicoes2 = (120, 1020)

        box_position_feed_else = (745, 1025)

        category_mapping = {
            'condicoes1': {
                'feed': 'peça_condicoes1_feed',
                'stories': 'peça_condicoes1_stories',
                'box_position_feed': box_position_feed_condicoes1,
                'box_position_stories':  box_position_stories_condicoes
            },
            'condicoes2': {
                'feed': 'peça_condicoes2_feed',
                'stories': 'peça_condicoes2_stories',
                'box_position_feed': box_position_feed_condicoes2,
                'box_position_stories': box_position_stories_condicoes
            },
            'investidor': {
                'feed': 'peça_investidor_feed',
                'stories': 'peça_investidor_stories',
                'box_position_feed': box_position_feed_general,
                'box_position_stories': box_position_stories_general
            },
            'localizacao': {
                'feed': 'peça_localizacao_feed',
                'stories': 'peça_localizacao_stories',
                'box_position_feed': box_position_feed_else,
                'box_position_stories': box_position_stories_general
            },
            'petplace': {
                'feed': 'peça_petplace_feed',
                'stories': 'peça_petplace_stories',
                'box_position_feed': box_position_feed_else,
                'box_position_stories': box_position_stories_general
            },
            'poliesportiva': {
                'feed': 'peça_poliesportiva_feed',
                'stories': 'peça_poliesportiva_stories',
                'box_position_feed': box_position_feed_else,
                'box_position_stories': box_position_stories_general
            },
            'general': {
                'feed': 'peça_general_feed',
                'stories': 'peça_general_stories',
                'box_position_feed': box_position_feed_general,
                'box_position_stories': box_position_stories_general
            },
            'playground': {
                'feed': 'peça_playground_feed',
                'stories': 'peça_playground_stories',
                'box_position_feed': box_position_feed_else,
                'box_position_stories': box_position_stories_general
            },
            'quadraAreia': {
                'feed': 'peça_quadraAreia_feed',
                'stories': 'peça_quadraAreia_stories',
                'box_position_feed': box_position_feed_else,
                'box_position_stories': box_position_stories_general
            },
            'areaLazer': {
                'feed': 'peça_areaLazer_feed',
                'stories': 'peça_areaLazer_stories',
                'box_position_feed': box_position_feed_else,
                'box_position_stories': box_position_stories_general
            }
        }

        # List to hold links for all generated images
        generated_images = []

        # Generate images for each selected category
        for category in categories:
            category_data = category_mapping.get(category)

            if category_data:
                feed_link = fileManager.generate_image(category_data['feed'], google_drive_template_folder_id, name, formatted_phone, creci, category_data['box_position_feed'])
                stories_link = fileManager.generate_image(category_data['stories'], google_drive_template_folder_id, name, formatted_phone, creci, category_data['box_position_stories'])

            generated_images.append({
                'category': category,
                'feed_image_url': feed_link,
                'stories_image_url': stories_link
            })

        google_api.add_to_google_sheet(data)
        fileManager.clean_up_temp_folder() 
        
        # Return the generated image URLs
        return jsonify({'generated_images': generated_images}), 200

    except AppError as e:
        print(e)
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        print(e)
        return jsonify({'message': 'Erro ao criar a peça. Por favor, tente novamente mais tarde.'}), 500

