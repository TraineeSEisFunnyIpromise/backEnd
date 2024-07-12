import unittest
import account.Authentication as app


class TestLoginEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_login_successful(self):
        # Define the test data (replace with valid credentials)
        test_data = {'username': 'admin', 'password': 'admin1'}

        # Make a POST request to the login endpoint
        response = self.app.post('/login', json=test_data)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the response contains the expected message
        self.assertIn('message', response.json)
        self.assertEqual(response.json['message'], 'Login successful')

    def test_login_invalid_credentials(self):
        # Define the test data (replace with invalid credentials)
        test_data = {'username': 'Dark', 'password': 'vanholmes69'}

        # Make a POST request to the login endpoint
        response = self.app.post('/login', json=test_data)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the response contains the expected error message
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], 'Invalid username or password')

if __name__ == '__main__':
    unittest.main()
