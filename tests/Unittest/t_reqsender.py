import unittest
from unittest.mock import patch

from Reqandscrape.Requestsender.chatgptreqsender import change_data

class TestChangeData(unittest.TestCase):
    def test_success_response(self):
        response = change_data("electric fan")
        # Assert the response structure and content
        self.assertIsInstance(response, dict)
        self.assertIn('choices', response)
        self.assertIn(True, response['choices'][0])

    def test_unsuccess_response(self):
        response = change_data("someinput")
        # Assert the response structure and content
        self.assertIsInstance(response, dict)
        self.assertIn('choices', response)
        self.assertIn(False, response['choices'][0])
    
    def test_success_response_boolean(self):
        response = change_data("student")
        # Assert the response structure and content
        self.assertIsInstance(response, dict)
        self.assertIn('choices', response)
        self.assertEqual('True', response['choices'][0])

    def test_unsuccess_response_boolean(self):
        response = change_data("someinput")
        # Assert the response structure and content
        self.assertIsInstance(response, dict)
        self.assertIn('choices', response)
        self.assertIn('False', response['choices'][0])

    def test_success_convert_input():
        return
    
    def test_unsuccess_convert_input():
        return