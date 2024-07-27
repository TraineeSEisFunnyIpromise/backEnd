from flask import Flask  # Optional, for clarity
import unittest
from MainApp import app  # Assuming your Flask app is in main.py

class TestLoginEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.username = 'test1'
        self.user_data = {'name': 'test1','password': '1234', 'About me':'ye', 'Question for reset password':'slurpy', 
'Answer for reset password':'slurp'}

    def test_login_successful(self):
        # Define the test data (replace with valid credentials)
        test_data = {'username': 'test1', 'password': '1234'}

        # Make a POST request to the login endpoint
        response = self.app.post('/login', json=test_data)
        print(response)

    def test_login_invalid_credentials(self):
        # Define the test data (replace with invalid credentials)
        test_data = {'username': 'Dark', 'password': 'vanholmes69'}

        # Make a POST request to the login endpoint
        response = self.app.post('/login', json=test_data)

        print(response)

if __name__ == '__main__':
    unittest.main()
