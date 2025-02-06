import os
import shutil
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
import time

from app.utils.utils_google_api import drive_service
from app.utils.utils_google_api import download_template_from_drive, upload_and_get_link
from app.app_error import AppError

load_dotenv()
google_drive_folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')

def clean_up_temp_folder():
    root_path = os.path.dirname(os.path.abspath(__file__))
    temp_dir = os.path.abspath(os.path.join(root_path, '..', '..', 'temp'))
    
    if os.path.exists(temp_dir):
        try:
            # List all files in temp_dir and remove them
            for file_name in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning up temp directory {temp_dir}: {e}")

def generate_image(file_name, folder_id, name, phone, creci, box_position):
    # Downloading template from Google Drive
    template_path = download_template_from_drive(file_name, folder_id)

    if template_path is None:
        print(f"Erro ao baixar o template '{file_name}'.")
        return None

    root_path = os.path.dirname(os.path.abspath(__file__))
    print(f"Root path: {root_path}")
    font_path_bold = os.path.join(root_path, '..', 'static', 'fonts', 'Lato-Bold.ttf')
    font_path_black = os.path.join(root_path, '..', 'static', 'fonts', 'Lato-Black.ttf')

    with Image.open(template_path) as image:
        draw = ImageDraw.Draw(image)
        
        box_width = 456
        box_height = 127
        margin = 15

        max_font_size = 35
        min_font_size = 10

        name_text = name
        creci_text = f"Creci: {creci.split('-')[-1]}-TO"
        phone_text = phone
        
        def adjust_font_size(text, max_width, font_path, max_font_size, min_font_size):
            font_size = max_font_size
            while font_size >= min_font_size:
                font = ImageFont.truetype(font_path, font_size)
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                if text_width <= max_width:
                    return font
                font_size -= 1
            return ImageFont.truetype(font_path, min_font_size)

        name_font = adjust_font_size(name_text, box_width - 2 * margin, font_path_black, max_font_size, min_font_size)
        creci_font = adjust_font_size(creci_text, box_width - 2 * margin, font_path_bold, max_font_size - 7, min_font_size)
        phone_font = adjust_font_size(phone_text, box_width - 2 * margin, font_path_black, max_font_size, min_font_size)

        name_height = draw.textbbox((0, 0), name_text, font=name_font)[3]
        creci_height = draw.textbbox((0, 0), creci_text, font=creci_font)[3]
        phone_height = draw.textbbox((0, 0), phone_text, font=phone_font)[3]

        line_spacing = 4

        total_text_height = name_height + creci_height + phone_height + 2 * line_spacing

        y_offset = (box_height - total_text_height) / 2

        # Calculate text position
        name_x = box_position[0] + (box_width - draw.textbbox((0, 0), name_text, font=name_font)[2]) / 2
        name_y = box_position[1] + margin + y_offset

        creci_x = box_position[0] + (box_width - draw.textbbox((0, 0), creci_text, font=creci_font)[2]) / 2
        creci_y = name_y + name_height + line_spacing

        phone_x = box_position[0] + (box_width - draw.textbbox((0, 0), phone_text, font=phone_font)[2]) / 2
        phone_y = creci_y + creci_height + line_spacing

        draw.text((name_x, name_y), name_text, font=name_font, fill="#FFFFFF")
        draw.text((creci_x, creci_y), creci_text, font=creci_font, fill="#FFFFFF")
        draw.text((phone_x, phone_y), phone_text, font=phone_font, fill="#FFFFFF")

        # Saves image
        output_filename = f"{name.replace(' ', '_')}_template.jpg"
        root_path = os.path.dirname(os.path.abspath(__file__))
        temp_dir = os.path.abspath(os.path.join(root_path, '..', '..', 'temp'))

        output_temp_path = os.path.join(temp_dir, output_filename)
        image.save(output_temp_path, format='JPEG')

    return upload_and_get_link(output_temp_path, output_filename, google_drive_folder_id, template_path)