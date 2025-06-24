from flask import Blueprint, request, jsonify
from flask import request, jsonify
from dotenv import load_dotenv

from app.utils.auth import token_required
from app.utils.utils_files import FileManager
from app.utils.utils_format import UserInputValidator
from app.utils.utils_google_api import GoogleAPI
from app.app_error import AppError

load_dotenv()

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
        selected_city = data.get('city', '')
        selected_enterprise = data.get('enterprise', '')

        if not name or not phone or not creci:
           raise AppError('Preencha todos os campos.', 400)
        
        if len(creci) < 4 or len(creci) > 5 or not creci.isdigit():
            raise AppError('Insira um código CRECI válido (4 a 5 dígitos numéricos).', 400)
        
        # Format the phone number
        formatted_phone = UserInputValidator.format_phone_number(phone)

        # Validates name
        UserInputValidator.validate_name(name)
        
        box_position_feed = (745, 1025)
        box_position_stories = (312, 1615)

        # List to hold links for all generated images
        generated_images = []

        enterprise_info = google_api.get_enterprise_data(selected_enterprise, selected_city)
        google_drive_template_folder_id = enterprise_info['folder_id']
        categories = data.get('categories') or enterprise_info['categorias']
        
        formatted_city = UserInputValidator.format_filename(selected_city)
        formatted_enterprise = UserInputValidator.format_filename(selected_enterprise)

        # Generate images for each selected category
        for category in categories:
            if category:
                feed_template = f"{category}_feed_{formatted_city}_{formatted_enterprise}"
                stories_template = f"{category}_stories_{formatted_city}_{formatted_enterprise}"

                feed_link = None
                stories_link = None
        
            try:
                feed_link = fileManager.generate_image(feed_template, google_drive_template_folder_id, 
                                                        name, formatted_phone, creci, box_position_feed)
            except AppError as e:
                print(e)
                
            try:
                stories_link = fileManager.generate_image(stories_template, google_drive_template_folder_id, 
                                                        name, formatted_phone, creci, box_position_stories)
            except AppError as e:
                stories_link = None

            generated_images.append({
                'category': category,
                'feed_image_url': feed_link,
                'stories_image_url': stories_link
            })

        # google_api.add_to_google_sheet(data)
        fileManager.clean_up_temp_folder() 
        
        # Return the generated image URLs
        return jsonify({'generated_images': generated_images}), 200

    except AppError as e:
        print(e)
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        print(e)
        return jsonify({'message': 'Erro ao criar a peça. Por favor, tente novamente mais tarde.'}), 500