import os
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
from app.utils.utils_google_api import GoogleAPI
from app.app_error import AppError

load_dotenv()
google_drive_output_folder_id = os.getenv('GOOGLE_DRIVE_OUTPUT_FOLDER_ID')

google_api = GoogleAPI()

class FileManager:
    def __init__(self):
        root_path = os.path.dirname(os.path.abspath(__file__))
        self.temp_dir = os.path.abspath(os.path.join(root_path, '..', '..', 'temp'))
        
        # Create temp directory if it doesn't exist
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

        self.font_path_bold = os.path.join(root_path, '..', 'static', 'fonts', 'Lato-Bold.ttf')
        self.font_path_black = os.path.join(root_path, '..', 'static', 'fonts', 'Lato-Black.ttf')
    
    def clean_up_temp_folder(self):
        if os.path.exists(self.temp_dir):
            try:
                for file_name in os.listdir(self.temp_dir):
                    file_path = os.path.join(self.temp_dir, file_name)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
            except Exception as e:
                print(f"Error cleaning up temp directory {self.temp_dir}: {e}")
    
    def adjust_font_size(self, text, max_width, font_path, max_font_size=35, min_font_size=10):
        font_size = max_font_size
        while font_size >= min_font_size:
            font = ImageFont.truetype(font_path, font_size)
            bbox = ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            if text_width <= max_width:
                return font
            font_size -= 1
        return ImageFont.truetype(font_path, min_font_size)
    
    def generate_image(self, file_name, folder_id, name, phone, creci, box_position):
        template_path = google_api.download_template_from_drive(file_name, folder_id)
        
        if template_path is None:
            raise AppError(f"Erro ao baixar o template '{file_name}'.")
        
        with Image.open(template_path) as image:
            draw = ImageDraw.Draw(image)
            box_width, box_height, margin = 456, 127, 15
            
            name_font = self.adjust_font_size(name, box_width - 2 * margin, self.font_path_black)
            creci_text = f"Creci: {creci.split('-')[-1]}"
            creci_font = self.adjust_font_size(creci_text, box_width - 2 * margin, self.font_path_bold, 28)
            phone_font = self.adjust_font_size(phone, box_width - 2 * margin, self.font_path_black)
            
            name_height = draw.textbbox((0, 0), name, font=name_font)[3]
            creci_height = draw.textbbox((0, 0), creci_text, font=creci_font)[3]
            phone_height = draw.textbbox((0, 0), phone, font=phone_font)[3]
            
            line_spacing = 4
            total_text_height = name_height + creci_height + phone_height + 2 * line_spacing
            y_offset = (box_height - total_text_height) / 2
            
            name_x = box_position[0] + (box_width - draw.textbbox((0, 0), name, font=name_font)[2]) / 2
            name_y = box_position[1] + margin + y_offset
            creci_x = box_position[0] + (box_width - draw.textbbox((0, 0), creci_text, font=creci_font)[2]) / 2
            creci_y = name_y + name_height + line_spacing
            phone_x = box_position[0] + (box_width - draw.textbbox((0, 0), phone, font=phone_font)[2]) / 2
            phone_y = creci_y + creci_height + line_spacing
            
            draw.text((name_x, name_y), name, font=name_font, fill="#FFFFFF")
            draw.text((creci_x, creci_y), creci_text, font=creci_font, fill="#FFFFFF")
            draw.text((phone_x, phone_y), phone, font=phone_font, fill="#FFFFFF")
            
            output_filename = f"{name.replace(' ', '_')}_template.jpg"
            output_temp_path = os.path.join(self.temp_dir, output_filename)
            image.save(output_temp_path, format='JPEG')
        
        return google_api.upload_and_get_link(output_temp_path, output_filename, google_drive_output_folder_id, template_path)
