from flask import Blueprint, jsonify
from dotenv import load_dotenv
import os

from app.utils.auth import token_required
from app.utils.utils_google_api import GoogleAPI
from app.app_error import AppError

load_dotenv()

data_bp = Blueprint('data', __name__)

google_api = GoogleAPI()

@data_bp.errorhandler(AppError)
@token_required
@data_bp.route('/get_data', methods=['GET'])
def get_data():
    try:
        gc = google_api.get_google_sheets_service()
        spreadsheet_id = os.getenv('GOOGLE_SHEET_CONFIG_ID')
        sh = gc.open_by_key(spreadsheet_id)

        # Aba 1: empreendimentos
        ws_emp = sh.worksheet('empreendimentos')
        all_rows = ws_emp.get_all_values()[1:]  # ignora cabeçalho
        filtered_rows = [row[:4] for row in all_rows if len(row) >= 4]

        # Aba 2: categorias (dicionário valor -> legenda)
        ws_cat = sh.worksheet('categorias')
        cat_rows = ws_cat.get_all_values()[1:]  # ignora cabeçalho
        cat_dict = {row[0].strip(): row[1].strip() for row in cat_rows if len(row) >= 2}

        response = []
        for row in filtered_rows:
            cod_categorias = [c.strip() for c in row[3].split(",") if c.strip()]
            legendas = [cat_dict.get(c, c) for c in cod_categorias] 

            response.append({
                "id": row[0],
                "empreendimento": row[1],
                "cidade": row[2],
                "categorias": cod_categorias,
                "legendas": legendas
            })

        return jsonify(response), 200

    except Exception as e:
        print(e)
        raise AppError("Não foi possível recuperar os dados dos Empreendimentos.", 404)

