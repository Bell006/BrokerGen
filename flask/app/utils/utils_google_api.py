import os
from google.oauth2 import service_account
import gspread
from googleapiclient.discovery import build
from datetime import datetime
from io import BytesIO
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from app.app_error import AppError

class GoogleAPI:
    def __init__(self):
        self.credentials_info = {
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

        self.credentials = service_account.Credentials.from_service_account_info(self.credentials_info)
        self.drive_service = build('drive', 'v3', credentials=self.credentials)

    def get_google_sheets_service(self):
        try:
            scopes = ['https://www.googleapis.com/auth/spreadsheets']
            credentials = service_account.Credentials.from_service_account_info(self.credentials_info, scopes=scopes)
            gc = gspread.authorize(credentials)
            
            return gc
        except Exception as e:
            print(f"Erro ao autorizar Google Sheets: {e}")
            raise AppError("Erro ao conectar com Google Sheets", 500)

    def add_to_google_sheet(self, data):
        gc = self.get_google_sheets_service()

        # Abrir a planilha pelo ID ou nome
        spreadsheet_id = os.getenv('GOOGLE_SHEET_ID')
        sh = gc.open_by_key(spreadsheet_id)

        worksheet = sh.sheet1

        current_date = datetime.now().strftime('%d/%m/%Y')

        worksheet.append_row([
            data['name'], 
            data['phone'], 
            data['creci'], 
            current_date  
        ])

    def get_file_id_by_name(self, file_name, folder_id):
        query = f"name='{file_name}.jpg' and '{folder_id}' in parents"
        results = self.drive_service.files().list(q=query, spaces="drive", fields="files(id, name)").execute()
        items = results.get('files', [])
        
        if not items:
            raise AppError(f"O arquivo '{file_name}' não foi encontrado na pasta no Google Drive.", 400)
        return items[0]['id']

    def download_template_from_drive(self, file_name, folder_id):
        try:
            file_id = self.get_file_id_by_name(file_name, folder_id)
            request = self.drive_service.files().get_media(fileId=file_id)

            # Temporary file path
            root_path = os.path.dirname(os.path.abspath(__file__))
            temp_dir = os.path.abspath(os.path.join(root_path, '..', '..', 'temp'))
            
            temp_file_path = os.path.join(temp_dir, file_name)

            fh = BytesIO()
            downloader = MediaIoBaseDownload(fd=fh, request=request)
            done = False
            
            while not done:
                status, done = downloader.next_chunk()

            # Save the file to the temporary path
            with open(temp_file_path, 'wb') as f:
                f.write(fh.getvalue())
            return temp_file_path

        except Exception as e:
            print(e)
            raise AppError(f"Erro ao gerar peças.", 500)

    def upload_and_get_link(self, output_temp_path, output_filename, google_drive_output_folder_id, template_path):
        # Upload to Google Drive
        file_metadata = {
            'name': output_filename,
            'parents': [google_drive_output_folder_id],
        }
        media = MediaFileUpload(output_temp_path, mimetype='image/jpeg', resumable=True)
        uploaded_file = self.drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        # Get link
        file_id = uploaded_file.get('id')
        file = self.drive_service.files().get(fileId=file_id, fields='webContentLink').execute()
        file_link = file.get('webContentLink')

        return file_link