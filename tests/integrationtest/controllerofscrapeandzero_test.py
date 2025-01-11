import json
from unittest.mock import patch

# Assuming your Flask application is in a file called app.py
from Reqandscrape.requestsender.chatgptreqsender import change_data as reqsender
from Reqandscrape.zeroshotclassify import calculate_the_zeroshot

# Sample data for testing
sample_search_criteria = "find laptops"
sample_user = "test_user"
sample_zeroshot_data = "This is some text for zeroshot classification"

def test_success_reqsender(self):
    result = reqsender("electric spoon")
    self.assertIsNotNone(result)
    
def test_unsuccess_reqsender(self):
    result = reqsender()
    self.assertIsNone(result)

def test_success_calculate_zeroshot(self):
    result = calculate_the_zeroshot()
    self.assertIsNotNone(result)
    
def test_unsuccess_calculate_zeroshot(self):
    result = calculate_the_zeroshot()
    self.assertIsNone(result)