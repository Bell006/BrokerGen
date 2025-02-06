import unittest
import json
from unittest.mock import patch, MagicMock

from app.app import app, google_api


class BrokerImagesTestCase(unittest.TestCase):
    
    def setUp(self):
        # Configura o ambiente de teste
        self.app = app.test_client()
        app.testing = True
        self.mock_google_api = google_api

    @patch('app.google_api.GoogleAPI.add_to_google_sheet')
    @patch('app.google_api.GoogleAPI.get_google_drive_service')
    def test_create_broker_images_valid(self, mock_get_google_drive_service, mock_add_to_google_sheet):

        mock_drive_service = MagicMock()
        mock_get_google_drive_service.return_value = mock_drive_service

        mock_drive_service.files().create().execute.return_value = {'id': 'mocked_file_id'}
        mock_drive_service.files().get().execute.return_value = {'webContentLink': 'https://mocked_link'}

        response = self.app.post('/create_image', 
                                    data=json.dumps({
                                        'name': 'John Doe',
                                        'phone': '11987654321',
                                        'creci': '1234',
                                        'categories': ['investidor', 'localizacao']
                                    }),
                                    content_type='application/json')

        # Verifica se a resposta contém a chave 'generated_images'
        response_json = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('generated_images', response_json)
        self.assertEqual(len(response_json['generated_images']), 2)

    def test_create_broker_images_missing_fields(self):
        response = self.app.post('/create_image', 
                                    data=json.dumps({
                                        'name': 'John Doe',
                                        'phone': '11987654321',
                                    }),
                                    content_type='application/json')

        # Verifica se a resposta tem o status code 400
        self.assertEqual(response.status_code, 400)

        # Verifica se a resposta contém uma mensagem de erro
        response_json = json.loads(response.data)
        self.assertEqual(response_json['message'], 'Preencha todos os campos.')

    def test_create_broker_images_invalid_creci(self):
        response = self.app.post('/create_image', 
                                    data=json.dumps({
                                        'name': 'John Doe',
                                        'phone': '11987654321',
                                        'creci': '12',
                                        'categories': ['investidor']
                                    }),
                                    content_type='application/json')

        # Verifica se a resposta tem o status code 400
        self.assertEqual(response.status_code, 400)

        # Verifica se a resposta contém uma mensagem de erro
        response_json = json.loads(response.data)
        self.assertEqual(response_json['message'], 'Insira um código CRECI válido (4 a 5 dígitos numéricos).')

if __name__ == '__main__':
    unittest.main()
