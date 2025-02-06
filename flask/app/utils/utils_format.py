import re
from app.app_error import AppError

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