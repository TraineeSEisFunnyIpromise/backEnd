import unittest
from unittest.mock import patch, MagicMock
import requests
from reqandscrape.requestsender.chatgptreqsender import change_data, extract_criteria, receiveinput

class TestChangeData(unittest.TestCase):

    @patch('reqandscrape.Requestsender.chatgptreqsender.requests.post')
    def test_success_change_data(self, mock_post):
        # Mock the response from the OpenAI API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'choices': [
                {
                    'message': {
                        'content': '1. Capacity\n2. Slot size\n3. Browning controls\n4. Features\n5. Ease of cleaning\n6. Budget\n7. Style'
                    }
                }
            ]
        }
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        input_text = "Toaster criteria"
        group_target = "general"
        result = change_data(input_text, group_target)
        self.assertIsNotNone(result)
        self.assertIn('1. Capacity', result)

    @patch('reqandscrape.Requestsender.chatgptreqsender.requests.post')
    def test_failure_change_data(self, mock_post):
        # Mock a failed response from the OpenAI API
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("API error")
        mock_post.return_value = mock_response

        input_text = "Toaster criteria"
        group_target = "general"
        result = change_data(input_text, group_target)
        self.assertIsNone(result)

    def test_extract_criteria(self):
        text = """1. Capacity: Do you usually toast for one or two people?
2. Slot size: Consider what types of bread you toast.
3. Browning controls: How precise do you want your toast?
4. Features: Do you want a defrost function for frozen bread?
5. Ease of cleaning: Look for a toaster with a removable crumb tray.
6. Budget: Toasters range in price from basic models to high-end ones.
7. Style: Some toasters come in a variety of styles to match your kitchen décor."""
        result = extract_criteria(text)
        self.assertEqual(result, ['1. Capacity', '2. Slot size', '3. Browning controls', '4. Features', '5. Ease of cleaning', '6. Budget', '7. Style'])


    @patch('reqandscrape.Requestsender.chatgptreqsender.change_data')
    @patch('reqandscrape.Requestsender.chatgptreqsender.check_input_word', return_value="true")
    def test_receiveinput(self, mock_check_input_word, mock_change_data):
        mock_change_data.return_value = """1. Capacity: Do you usually toast for one or two people?
    2. Slot size: Consider what types of bread you toast.
    3. Browning controls: How precise do you want your toast?
    4. Features: Do you want a defrost function for frozen bread?
    5. Ease of cleaning: Look for a toaster with a removable crumb tray.
    6. Budget: Toasters range in price from basic models to high-end ones.
    7. Style: Some toasters come in a variety of styles to match your kitchen décor."""
        
        input_text = "Toaster criteria"
        group_target = "general"
        result = receiveinput(input_text, group_target)
        self.assertIsNotNone(result)
        self.assertEqual(result, ['1. Capacity', '2. Slot size', '3. Browning controls', '4. Features', '5. Ease of cleaning', '6. Budget', '7. Style'])

if __name__ == '__main__':
    unittest.main()