import unittest
from unittest.mock import patch

from reqandscrape.chatgptreqsender import change_data

class TestChangeData(unittest.TestCase):
    def test_successful_response(self):
        response = change_data("some input")
        # Assert the response structure and content (modify based on actual response format)
        self.assertIsInstance(response, dict)
        self.assertIn('choices', response)
        self.assertIn('message', response['choices'][0])

