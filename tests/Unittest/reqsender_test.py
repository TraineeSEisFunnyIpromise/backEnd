import unittest
import requests
from Reqandscrape.requestsender.chatgptreqsender import change_data, extract_criteria, receiveinput,check_input_word

class TestChangeData(unittest.TestCase):


    def test_success_change_data(self):
        # Mock the response from the OpenAI API


        input_text = "Toaster criteria"
        group_target = "general"
        result = change_data(input_text, group_target)
        self.assertIsNotNone(result)
        self.assertIn('1. Capacity', result)


    def test_failure_change_data(self):
        # Mock a failed response from the OpenAI API


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



    def test_receiveinput(self):

        input_text = "Toaster criteria"
        group_target = "general"
        result = receiveinput(input_text, group_target)
        self.assertIsNotNone(result)

    def test_checkinput_word(self):

        input_text = "Toaster criteria"
        group_target = "general"
        result = check_input_word(input_text, group_target)
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()