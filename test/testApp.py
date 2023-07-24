# test_app.py

import unittest
from Flask_login import app

class TestLogin(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_valid_login(self):
        # Test valid login credentials
        response = self.app.post('/login', json={'username': 'admin', 'password': 'admin1'})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Login successful')

    def test_invalid_login(self):
        # Test invalid login credentials
        response = self.app.post('/login', json={'username': 'user', 'password': 'wrongpassword'})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['error'], 'Invalid username or password')

if __name__ == '__main__':
    unittest.main()
        
class TestApp_2():
        
    def test_deleteUser(self):
        # Test case for some_function_to_test
        result = some_function_to_test(3, 5)
        self.assertEqual(result, 8)
        
    def test_resetPassword(self):
        # Test case for some_function_to_test
        result = some_function_to_test(3, 5)
        self.assertEqual(result, 8)
        
class TestApp_FB():
        
    def test_Scraped_Data_FB(self):
        # Test case for some_function_to_test
        result = some_function_to_test(3, 5)
        self.assertEqual(result, 8)
        
    def test_Scraped_ID_FB(self):
        # Test case for some_function_to_test
        result = some_function_to_test(3, 5)
        self.assertEqual(result, 8)

if __name__ == '__main__':
    unittest.main()
