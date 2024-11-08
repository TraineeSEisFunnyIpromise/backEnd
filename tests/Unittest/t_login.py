from flask import Flask  # Optional, for clarity
import unittest
from MainApp import app  # Assuming your Flask app is in main.py

class TestLoginEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.username = 'test1'
        self.user_data = {'name': 'test1','password': '1234', 'About me':'ye', 'Question for reset password':'slurpy', 
'Answer for reset password':'slurp'}



  
    def test_successful_authentication(self, mock_access_database, mock_check_username, mock_check_database_status):
        result = authentication('testuser', 'testpassword')
        self.assertIsNotNone(result)
        self.assertEqual(result['username'], 'testuser')

 
    def test_failed_authentication(self, mock_access_database, mock_check_username, mock_check_database_status):
        result = authentication('testuser', 'wrongpassword')
        self.assertIsInstance(result, tuple)
        self.assertEqual(result[1], 400)

    def test_successful_reset_password():
        result = ""
        
    def test_fail_reset_password():
        result = ""

    def test_successful_register_newuser():
        result = ""

    def test_fail_register_newuser():
        result = ""


if __name__ == '__main__':
    unittest.main()
