import os
from flask import request, jsonify, Flask
from flask_cors import CORS
from dotenv import load_dotenv

from app.utils import format_phone_number, validate_name, generate_image
from app.app_error import AppError

##Setting application
app = Flask(__name__)
CORS(app)

load_dotenv()
google_drive_folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
    
@app.errorhandler(AppError)

@app.route('/create_image', methods=['POST'])

def create_broker_images():
    try:

        data = request.get_json()

        phone = data.get('phone', '')
        name = data.get('name', '').upper()
        creci = data.get('creci', '').upper()
        categories = data.get('categories', [])

        if not name or not phone or not creci:
           raise AppError('Preencha todos os campos.', 400)
        
        # Format the phone number
        formatted_phone = format_phone_number(phone)

        # Validates name
        validate_name(name)

        font_path_bold = os.path.join(app.root_path, 'static', 'fonts', 'Lato-Bold.ttf')
        
        box_position_feed = (142, 1020)
        box_position_stories = (310, 1620)

        box_position_stories_condicoes = (120, 1600)
        box_position_feed_condicoes1 = (718, 970)
        box_position_feed_condicoes2 = (120, 1020)

        box_position_feed_else = (725, 1050)

        # List to hold links for all generated images
        generated_images = []

        # Generate images for each selected category
        for category in categories:
            template_image_path_feed = os.path.join(app.root_path, 'static', 'assets', f'peça_{category}_feed.jpg')
            template_image_path_stories = os.path.join(app.root_path, 'static', 'assets', f'peça_{category}_stories.jpg')

            if category == 'condicoes1':
                feed_link = generate_image(template_image_path_feed, name, formatted_phone,  font_path_bold, box_position_feed_condicoes1)
                stories_link = generate_image(template_image_path_stories, name, formatted_phone,  font_path_bold, box_position_stories_condicoes)
            elif category == 'condicoes2':
                feed_link = generate_image(template_image_path_feed, name, formatted_phone,  font_path_bold, box_position_feed_condicoes2)
                stories_link = generate_image(template_image_path_stories, name, formatted_phone,  font_path_bold, box_position_stories_condicoes)
            elif category == 'general' or category == 'investidor':
                feed_link = generate_image(template_image_path_feed, name, formatted_phone,  font_path_bold, box_position_feed)
                stories_link = generate_image(template_image_path_stories, name, formatted_phone,  font_path_bold, box_position_stories)
            else:
                feed_link = generate_image(template_image_path_feed, name, formatted_phone,  font_path_bold, box_position_feed_else)
                stories_link = generate_image(template_image_path_stories, name, formatted_phone,  font_path_bold, box_position_stories)

            generated_images.append({
                'category': category,
                'feed_image_url': feed_link,
                'stories_image_url': stories_link
            })

        # Return the generated image URLs
        return jsonify({'generated_images': generated_images}), 200

    
    except AppError as e:
        print(e)
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        print(e)
        return jsonify({'message': 'Erro ao criar a peça. Por favor, tente novamente mais tarde.'}), 500

if __name__ == '__main__':
    app.run(debug=True)