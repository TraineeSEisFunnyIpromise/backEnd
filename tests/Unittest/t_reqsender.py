import unittest
from unittest.mock import patch

from Reqandscrape.Requestsender.chatgptreqsender import change_data

class TestChangeData(unittest.TestCase):
    def test_successful_response(self):
        response = change_data("electric fan")
        # Assert the response structure and content (modify based on actual response format)
        self.assertIsInstance(response, dict)
        self.assertIn('choices', response)
        self.assertIn('message', response['choices'][0])

    def test_unsuccessful_response(self):
        response = change_data("someinput")
        # Assert the response structure and content (modify based on actual response format)
        self.assertIsInstance(response, dict)
        self.assertIn('choices', response)
        self.assertIn('message', response['choices'][0])
    
    def test_successful_response_boolean(self):
        response = change_data("student")
        # Assert the response structure and content (modify based on actual response format)
        self.assertIsInstance(response, dict)
        self.assertIn('choices', response)
        self.assertIn('message', response['choices'][0])

    def test_unsuccessful_response_boolean(self):
        response = change_data("someinput")
        # Assert the response structure and content (modify based on actual response format)
        self.assertIsInstance(response, dict)
        self.assertIn('choices', response)
        self.assertIn('message', response['choices'][0])