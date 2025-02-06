import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

from app.app import app
from app.utils.utils_google_api import GoogleAPI
from app.app_error import AppError

class TestGoogleAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        self.mock_credentials = MagicMock() 
        self.google_api = GoogleAPI()

        self.mock_credentials_info = {
            "spreadsheet_id": "mock_spreadsheet_id",
            "folder_id": "mock_folder_id"
        }

        self.google_api.credentials_info = self.mock_credentials_info


    @patch('gspread.authorize')
    @patch('google.oauth2.service_account.Credentials.from_service_account_info')
    def test_get_google_sheets_service(self, mock_from_service_account_info, mock_authorize):
        mock_credentials = MagicMock()
        mock_from_service_account_info.return_value = mock_credentials

        mock_gc = MagicMock()
        mock_authorize.return_value = mock_gc

        gc = self.google_api.get_google_sheets_service()

        self.assertEqual(gc, mock_gc)
        mock_authorize.assert_called_once_with(mock_credentials)

    @patch('app.utils.utils_google_api.GoogleAPI.get_google_sheets_service')
    @patch('os.getenv')
    def test_add_to_google_sheet(self, mock_getenv, mock_get_google_sheets_service):
        mock_gc = MagicMock()
        mock_spreadsheet = MagicMock()
        mock_worksheet = MagicMock()

        mock_get_google_sheets_service.return_value = mock_gc
        mock_gc.open_by_key.return_value = mock_spreadsheet
        mock_spreadsheet.sheet1 = mock_worksheet

        mock_getenv.return_value = "mock_spreadsheet_id"

        data = {
            'name': 'Test User',
            'phone': '123456789',
            'creci': '12345'
        }

        self.google_api.add_to_google_sheet(data)

        mock_get_google_sheets_service.assert_called_once()
        mock_gc.open_by_key.assert_called_once_with("mock_spreadsheet_id")
        current_date = datetime.now().strftime('%d/%m/%Y')
        mock_worksheet.append_row.assert_called_once_with([
            data['name'], 
            data['phone'], 
            data['creci'], 
            current_date
        ])

    @patch('googleapiclient.discovery.build')
    def test_get_file_id_by_name(self, mock_build):
        mock_drive_service = MagicMock()
        mock_files = mock_drive_service.files()
        mock_files.list.return_value.execute.return_value = {
            'files': [{'id': 'mock_file_id', 'name': 'mock_file_name.jpg'}]
        }
        self.google_api.drive_service = mock_drive_service

        file_id = self.google_api.get_file_id_by_name('mock_file_name', 'mock_folder_id')

        self.assertEqual(file_id, 'mock_file_id')
        mock_files.list.assert_called_once_with(
            q="name='mock_file_name.jpg' and 'mock_folder_id' in parents", 
            spaces="drive", 
            fields="files(id, name)"
        )

if __name__ == '__main__':
    unittest.main()