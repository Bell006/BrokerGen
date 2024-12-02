import re
import os
import tempfile
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
from googleapiclient.http import MediaFileUpload
from app.google_api import add_to_google_sheet, drive_service

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

def generate_image(template_path, name, phone, font_path_bold, box_position):
    # Open the template image
    image = Image.open(template_path)

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    box_width = 456
    box_height = 127
    box_radius = 32

    draw_rounded_rectangle(
        draw=draw,
        xy=box_position,
        width=box_width,
        height=box_height,
        radius=box_radius,
        outline="#FFFFFF",
        fill=None,
        border_width=1,
    )

    # Font config
    max_font_size = 35
    min_font_size = 10
    margin = 15

    # Área útil do retângulo
    inner_width = box_width - 2 * margin
    inner_height = box_height - 2 * margin

    # Textos a serem desenhados
    name_text = name
    phone_text = phone

    # Ajustar fonte para nome
    font_size = max_font_size
    while font_size >= min_font_size:
        font_name = ImageFont.truetype(font_path_bold, font_size)
        bbox = draw.textbbox((0, 0), name_text, font=font_name)
        name_width, name_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

        # Verificar se o texto se aproxima das bordas laterais
        if name_width <= inner_width and name_height <= inner_height / 2:
            if (inner_width - name_width) / 2 >= 15:  # Distância da borda
                break
        font_size -= 1

    # Ajustar fonte para telefone
    font_size = max_font_size
    while font_size >= min_font_size:
        font_phone = ImageFont.truetype(font_path_bold, font_size)
        bbox = draw.textbbox((0, 0), phone_text, font=font_phone)
        phone_width, phone_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

        # Verificar se o texto se aproxima das bordas laterais
        if phone_width <= inner_width and phone_height <= inner_height / 2:
            if (inner_width - phone_width) / 2 >= 15:  # Distância da borda
                break
        font_size -= 1

    # Calcular a altura total do texto (nome + telefone + espaço entre eles)
    total_text_height = name_height + phone_height + 20

    # Calcular posição vertical centralizada no retângulo
    total_y_offset = (inner_height - total_text_height) / 2

    # Calcular posições centralizadas para nome e telefone
    name_x = box_position[0] + (box_width - name_width) / 2
    name_y = box_position[1] + margin + total_y_offset

    phone_x = box_position[0] + (box_width - phone_width) / 2
    phone_y = name_y + name_height + 10

    # Desenhar textos
    draw.text((name_x, name_y), name_text, font=font_name, fill="#FFFFFF")
    draw.text((phone_x, phone_y), phone_text, font=font_phone, fill="#FFFFFF")

    temp_image_path = os.path.join('static', 'temp_image.jpg')
    image.save(temp_image_path)

    template_base_name = os.path.basename(template_path)
    template_name, _ = os.path.splitext(template_base_name)

    # Final name
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

