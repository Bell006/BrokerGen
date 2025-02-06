import unittest
from unittest.mock import patch, MagicMock
import os
from PIL import ImageFont

from app.utils.utils_files import FileManager

class TestFileManager(unittest.TestCase):
    def setUp(self):
        self.file_manager = FileManager()

    @patch('PIL.Image.open')
    @patch('app.utils.utils_google_api.GoogleAPI.download_template_from_drive')
    @patch('app.utils.utils_google_api.GoogleAPI.upload_and_get_link')
    def test_generate_image(self, mock_upload, mock_download, mock_open):
        mock_download.return_value = 'template_path'
        mock_image = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_image
        mock_upload.return_value = 'http://example.com/image.jpg'
        
        result = self.file_manager.generate_image('template.jpg', 'folder_id', 'John Doe', '1234567890', '1234-TO', (0, 0))
        
        self.assertEqual(result, 'http://example.com/image.jpg')
        mock_download.assert_called_once_with('template.jpg', 'folder_id')
        mock_upload.assert_called_once()


if __name__ == '__main__':
    unittest.main()