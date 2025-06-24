import re
from app.app_error import AppError
import unicodedata

class UserInputValidator:
    @staticmethod
    def format_phone_number(phone):
        digits = re.sub(r'\D', '', phone)

        if digits.startswith('0'):
            digits = digits[1:]

        if len(digits) < 10 or len(digits) > 11:
            raise AppError("Informe um número válido.\n(Celular: DDD + 9 + número)", 400)

        if len(digits) == 10 and digits[2] in '6789':
            digits = digits[:2] + '9' + digits[2:]

        return f"({digits[:2]}) {digits[2]} {digits[3:7]}-{digits[7:]}" if len(digits) == 11 else digits

    @staticmethod
    def validate_name(name):
        words = name.split()

        if len(words) < 2 or len(words) > 3:
            raise AppError("Insira apenas o primeiro nome e um sobrenome.", 400)
        
    @staticmethod
    def format_filename(text):
        if not text:
            return ""
        # Se houver barra, pega apenas a parte antes dela
        if "/" in text:
            text = text.split("/")[0]
        text = text.lower().strip()
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
        text = text.replace(" ", "").replace("-", "")
        return text
