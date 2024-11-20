from flask import Flask  # Optional, for clarity
import unittest
from MainApp import app  # Assuming your Flask app is in main.py
from account.Authentication import authentication,register_newuser,resetpassword

class TestLoginEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.username = 'test1'
        self.user_data = {'name': 'test1','password': '1234', 'About me':'ye', 'Question for reset password':'slurpy', 
'Answer for reset password':'slurp'}

    def test_successful_authentication(self):
        result = authentication('testuser', 'testpassword')
        self.assertIsNotNone(result)
        self.assertEqual(result['username'], 'testuser')

    def test_failed_authentication(self):
        result = authentication('testuser', 'wrongpassword')
        self.assertIsInstance(result, tuple)
        self.assertEqual(result[1], 400)

    def test_successful_reset_password(self):
        result = resetpassword('testuser','slurp' ,'testpassword')
        self.assertIsNotNone(result)
        self.assertEqual(result, 'Reset password successful')
        
    def test_fail_reset_password(self):
        result = resetpassword('testuser','slurpy' ,'testpassword')
        self.assertIsNotNone(result)
        self.assertEqual(result, 'Please provide correct username and password')

    def test_successful_register_newuser(self):
        user_data = {'name': 'test2','password': '123487', 'About me':'yeasda', 'Question for reset password':'slurpy', 
'Answer for reset password':'slurp'}
        result = register_newuser(user_data)
        self.assertIsNotNone(result)
        self.assertEqual(result, 'User created successfully')

    def test_fail_register_newuser(self):
        user_data = {'name': 'test1','password': '1234', 'About me':'ye', 'Question for reset password':'slurpy', 
'Answer for reset password':'slurp'}
        result = register_newuser(user_data)
        self.assertIsNotNone(result)
        self.assertEqual(result, 'Username already exists')


if __name__ == '__main__':
    unittest.main()
