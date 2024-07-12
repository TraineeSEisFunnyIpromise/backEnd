import unittest
import MainApp as app


class TestLoginEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_login_successful(self):
        # Define the test data (replace with valid credentials)
        test_data = {'username': 'admin', 'password': '1234'}

        # Make a POST request to the login endpoint
        response = self.app.post('/auth/login', json=test_data)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assertions to access and verify the username
        self.assertEqual(response.json['message'], 'Login successful')  # Assuming success message
        
        # Access the username from the request data (assuming it's accessible)
        request_data = self.app.application.last_json  # Get last request data (for testing)
        extracted_username = request_data['username']  # Access username from request data
        self.assertEqual(extracted_username, 'admin')  # Assert the extracted username

    def test_login_invalid_credentials(self):
        # Define the test data (replace with invalid credentials)
        test_data = {'username': 'Dark', 'password': 'vanholmes69'}

        # Make a POST request to the login endpoint
        response = self.app.post('/auth/login', json=test_data)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the response contains the expected error message
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], 'Invalid username or password')

if __name__ == '__main__':
    unittest.main()
