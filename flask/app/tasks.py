# app/tasks.py
from celery import Celery
from app.utils.utils_google_api import GoogleAPI
from app.utils.utils_files import FileManager
from app.utils.utils_format import UserInputValidator
from app.app_error import AppError
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery('tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'  
)

google_api = GoogleAPI()
fileManager = FileManager()

@celery_app.task(bind=True)
def generate_image_task(self, data):
    try:
        phone = data.get('phone', '')
        name = data.get('name', '').upper()
        creci = data.get('creci', '')
        categories = data.get('categories', [])
        selected_city = data.get('city', '')
        selected_enterprise = data.get('enterprise', '')

        if not name or not phone or not creci:
            raise ValueError('Preencha todos os campos.') 

        if len(creci) < 4 or len(creci) > 5 or not creci.isdigit():
            raise ValueError('Insira um código CRECI válido (4 a 5 dígitos numéricos).')

        formatted_phone = UserInputValidator.format_phone_number(phone)
        UserInputValidator.validate_name(name)

        generated_images = []

        enterprise_info = google_api.get_enterprise_data(selected_enterprise, selected_city)
        folder_id = enterprise_info['folder_id']
        categories = data.get('categories') or enterprise_info['categorias'] or []

        formatted_city = UserInputValidator.format_filename(selected_city)
        formatted_enterprise = UserInputValidator.format_filename(selected_enterprise)

        for category in categories:
            image_data = {'category': category, 'feed_image_url': None, 'stories_image_url': None}

            try:
                feed_template = f"{category}_feed_{formatted_city}_{formatted_enterprise}"
                image_data['feed_image_url'] = fileManager.generate_image(
                    feed_template, folder_id, name, formatted_phone, creci, (745, 1025)
                )
            except AppError as e:
                print(e)

            try:
                stories_template = f"{category}_stories_{formatted_city}_{formatted_enterprise}"
                image_data['stories_image_url'] = fileManager.generate_image(
                    stories_template, folder_id, name, formatted_phone, creci, (312, 1615)
                )
            except AppError as e:
                print(e)

            generated_images.append(image_data)

        fileManager.clean_up_temp_folder()

        return {'status': 'success', 'generated_images': generated_images}

    except Exception as e:
        raise ValueError(str(e))
