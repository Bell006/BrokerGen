# google_api.py
import os
from google.oauth2 import service_account
import gspread
from googleapiclient.discovery import build
from datetime import datetime
from app.app_error import AppError

# Create credentials_info dictionary from environment variables
credentials_info = {
    "type": os.getenv('TYPE'),
    "project_id": os.getenv('PROJECT_ID'),
    "private_key_id": os.getenv('PRIVATE_KEY_ID'),
    "private_key": os.getenv('PRIVATE_KEY'),
    "client_email": os.getenv('CLIENT_EMAIL'),
    "client_id": os.getenv('CLIENT_ID'),
    "auth_uri": os.getenv('AUTH_URI'),
    "token_uri": os.getenv('TOKEN_URI'),
    "auth_provider_x509_cert_url": os.getenv('AUTH_PROVIDER_X509_CERT_URL'),
    "client_x509_cert_url": os.getenv('CLIENT_X509_CERT_URL'),
    "universe_domain": "googleapis.com"
}

def get_google_sheets_service():
    try:
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=scopes)
        gc = gspread.authorize(credentials)
        
        return gc
    except Exception as e:
        print(f"Erro ao autorizar Google Sheets: {e}")
        raise AppError("Erro ao conectar com Google Sheets", 500)

def add_to_google_sheet(data):
    gc = get_google_sheets_service()

    # Abrir a planilha pelo ID ou nome
    spreadsheet_id = os.getenv('GOOGLE_SHEET_ID')
    sh = gc.open_by_key(spreadsheet_id)

    worksheet = sh.sheet1

    email = data.get('email')
    existing_rows = worksheet.get_all_records()
    
    row_to_delete = None
    for index, row in enumerate(existing_rows):
        if row['Email'].strip().lower() == email.strip().lower():
            row_to_delete = index + 2  
            break

    if row_to_delete:
        worksheet.delete_rows(row_to_delete)

    current_date = datetime.now().strftime('%d/%m/%Y')

    worksheet.append_row([
        data['name'], 
        data['phone'], 
        data['department'], 
        current_date  
    ])

# Inicializar Google Drive Service
credentials = service_account.Credentials.from_service_account_info(credentials_info)
drive_service = build('drive', 'v3', credentials=credentials)