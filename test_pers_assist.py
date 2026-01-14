import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Добавить директорию проекта в путь
sys.path.insert(0, os.path.dirname(__file__))

import pers_assist

class TestPersonalAssistant(unittest.TestCase):

    def test_generate_response_success(self):
        with patch('pers_assist.requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.json.return_value = {'choices': [{'message': {'content': 'Test response'}}]}
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response

            result = pers_assist.generate_response("Hello")
            self.assertEqual(result, "Test response")

    def test_generate_response_timeout(self):
        with patch('pers_assist.requests.post', side_effect=pers_assist.requests.RequestException("Timeout")):
            result = pers_assist.generate_response("Hello")
            self.assertIn("Извините", result)

    def test_is_speech(self):
        # Тест с валидным фреймом
        frame = b'\x00\x01' * 160  # 320 байт для 20мс при 16кГц
        result = pers_assist.is_speech(frame)
        self.assertIsInstance(result, bool)

if __name__ == '__main__':
    unittest.main()