import json
from unittest.mock import patch

# Assuming your Flask application is in a file called app.py
from Reqandscrape.requestsender.chatgptreqsender import change_data as reqsender
from Reqandscrape.zeroshotclassify import calculate_the_zeroshot

# Sample data for testing
sample_search_criteria = "find laptops"
sample_user = "test_user"
sample_zeroshot_data = "This is some text for zeroshot classification"

@patch('Reqandscrape.requestsender.chatgptreqsender.change_data')
def test_success_reqsender(self, mock_reqsender):
        # Mock the return value of reqsender
        mock_reqsender.return_value = {"response": "mocked response"}
        
        result = reqsender("electric spoon")
        self.assertIsNotNone(result)
        self.assertEqual(result, {"response": "mocked response"})
    
@patch('Reqandscrape.requestsender.chatgptreqsender.change_data')
def test_unsuccess_reqsender(self, mock_reqsender):
        # Mock the return value of reqsender to be None
        mock_reqsender.return_value = None
        
        result = reqsender()
        self.assertIsNone(result)

@patch('Reqandscrape.zeroshotclassify.calculate_the_zeroshot')
def test_success_calculate_zeroshot(self, mock_calculate):
        # Mock the return value of calculate_the_zeroshot
        mock_calculate.return_value = {"classification": "mocked classification"}
        
        result = calculate_the_zeroshot()
        self.assertIsNotNone(result)
        self.assertEqual(result, {"classification": "mocked classification"})
    
@patch('Reqandscrape.zeroshotclassify.calculate_the_zeroshot')
def test_unsuccess_calculate_zeroshot(self, mock_calculate):
        # Mock the return value of calculate_the_zeroshot to be None
        mock_calculate.return_value = None
        
        result = calculate_the_zeroshot()
        self.assertIsNone(result)