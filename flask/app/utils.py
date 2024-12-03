import re
import os
import tempfile
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
from googleapiclient.http import MediaFileUpload
from app.google_api import drive_service

from app.app_error import AppError

load_dotenv()
google_drive_folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')

def format_phone_number(phone):
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)

    # Remove leading zero if present
    if digits.startswith('0'):
        digits = digits[1:]

    if len(digits) < 10 or len(digits) > 11:
        raise AppError("Informe um número válido.\n(Celular: DDD + 9 + número", 400)
    
    if len(digits) == 10 and digits[2] in '6789':
        digits = digits[:2] + '9' + digits[2:]
    
    # Format based on length
    if len(digits) == 11:  # Mobile number
        formatted_phone = f"({digits[:2]}) {digits[2]} {digits[3:7]}-{digits[7:]}"
    
    return formatted_phone

def validate_name(name):
    # Split the name into words
    words = name.split()
    
    # Check the number of words
    if len(words) < 2 or len(words) > 3:
        raise AppError("Insira apenas o primeiro nome e um sobrenome.", 400)

def draw_rounded_rectangle(draw, xy, width, height, radius, outline, fill=None, border_width=1):
    x, y = xy
    right = x + width
    bottom = y + height

    # Círculos para cantos
    draw.arc([x, y, x + 2 * radius, y + 2 * radius], 180, 270, fill=outline, width=border_width)
    draw.arc([right - 2 * radius, y, right, y + 2 * radius], 270, 360, fill=outline, width=border_width)
    draw.arc([x, bottom - 2 * radius, x + 2 * radius, bottom], 90, 180, fill=outline, width=border_width)
    draw.arc([right - 2 * radius, bottom - 2 * radius, right, bottom], 0, 90, fill=outline, width=border_width)

    # Retângulos entre cantos
    draw.line([(x + radius, y), (right - radius, y)], fill=outline, width=border_width)  # Topo
    draw.line([(x + radius, bottom), (right - radius, bottom)], fill=outline, width=border_width)  # Base
    draw.line([(x, y + radius), (x, bottom - radius)], fill=outline, width=border_width)  # Esquerda
    draw.line([(right, y + radius), (right, bottom - radius)], fill=outline, width=border_width)  # Direita

    # Preenchimento
    if fill:
        draw.rectangle([x + radius, y + radius, right - radius, bottom - radius], fill=fill)

def generate_image(template_path, name, phone, creci, box_position):

    root_path = os.path.dirname(os.path.abspath(__file__))
    font_path_bold = os.path.join(root_path, 'static', 'fonts', 'Lato-Bold.ttf')
    font_path_black = os.path.join(root_path, 'static', 'fonts', 'Lato-Black.ttf')

    # Abrir a imagem de template
    image = Image.open(template_path)

    # Criar um contexto de desenho
    draw = ImageDraw.Draw(image)

    box_width = 456
    box_height = 127
    margin = 15

    # Configuração das fontes
    max_font_size = 35
    min_font_size = 10

    # Textos a serem desenhados
    name_text = name
    creci_text = f"Creci: {creci.split('-')[-1]}-TO"
    phone_text = phone
    
    # Função auxiliar para ajustar fonte ao espaço
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

    # Ajustar fontes para cada texto
    name_font = adjust_font_size(name_text, box_width - 2 * margin, font_path_black, max_font_size, min_font_size)
    creci_font = adjust_font_size(creci_text, box_width - 2 * margin, font_path_bold, max_font_size - 7, min_font_size)
    phone_font = adjust_font_size(phone_text, box_width - 2 * margin, font_path_black, max_font_size, min_font_size)

    # Determinar as alturas dos textos
    name_height = draw.textbbox((0, 0), name_text, font=name_font)[3]
    creci_height = draw.textbbox((0, 0), creci_text, font=creci_font)[3]
    phone_height = draw.textbbox((0, 0), phone_text, font=phone_font)[3]

    # Diminuir espaçamento entre as linhas
    line_spacing = 4

    total_text_height = name_height + creci_height + phone_height + 2 * line_spacing

    # Posição vertical centralizada dentro do box
    y_offset = (box_height - total_text_height) / 2

    # Calcular posições dos textos
    name_x = box_position[0] + (box_width - draw.textbbox((0, 0), name_text, font=name_font)[2]) / 2
    name_y = box_position[1] + margin + y_offset

    creci_x = box_position[0] + (box_width - draw.textbbox((0, 0), creci_text, font=creci_font)[2]) / 2
    creci_y = name_y + name_height + line_spacing

    phone_x = box_position[0] + (box_width - draw.textbbox((0, 0), phone_text, font=phone_font)[2]) / 2
    phone_y = creci_y + creci_height + line_spacing

    # Desenhar os textos na imagem
    draw.text((name_x, name_y), name_text, font=name_font, fill="#FFFFFF")
    draw.text((creci_x, creci_y), creci_text, font=creci_font, fill="#FFFFFF")
    draw.text((phone_x, phone_y), phone_text, font=phone_font, fill="#FFFFFF")

    # Salvar a imagem
    template_base_name = os.path.basename(template_path)
    template_name, _ = os.path.splitext(template_base_name)
    output_filename = f"{name.replace(' ', '_')}_{template_name}.jpg"


    # Save image
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
        output_path = temp_file.name
        image.save(output_path, format='JPEG')

        # Google Drive upload
        file_metadata = {
            'name': output_filename,
            'parents': [google_drive_folder_id],
        }
        media = MediaFileUpload(output_path, mimetype='image/jpeg', resumable=True)
        uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        # Get link
        file_id = uploaded_file.get('id')
        file = drive_service.files().get(fileId=file_id, fields='webContentLink').execute()
        file_link = file.get('webContentLink')

    return file_link

