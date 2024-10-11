import unittest
from unittest.mock import patch, MagicMock

from account.Authentication import app, usercollection


class LoginTest(unittest.TestCase):



    def setUp(self):
        self.app = app.test_client()
        self.usercollection = usercollection

    @patch('Authentication.is_mongodb_available')
    def test_successful_login(self, mock_mongodb_available):
        # Mock the is_mongodb_available function to return True
        mock_mongodb_available.return_value = True

        # Create a test user in the database
        test_user = {
            "username": "test_user",
            "password": "test_password"
        }
        self.usercollection.insert_one(test_user)

        # Login data
        login_data = {
            "username": "test_user",
            "password": "test_password"
        }

        # Send a POST request to the login endpoint
        response = self.app.post('/login', json=login_data)

        # Assert that the response is successful (202 Accepted)
        self.assertEqual(response.status_code, 202)

        # Assert that the session contains the username
        self.assertIn('username', response.json)
        self.assertEqual(response.json['username'], test_user['username'])

        # Clean up the test user
        self.usercollection.delete_one({"username": "test_user"})

    @patch('Authentication.is_mongodb_available')
    def test_incorrect_password(self, mock_mongodb_available):
        # Mock the is_mongodb_available function to return True
        mock_mongodb_available.return_value = True

        # Create a test user in the database
        test_user = {
            "username": "test_user",
            "password": "correct_password"
        }
        self.usercollection.insert_one(test_user)

        # Login data with incorrect password
        login_data = {
            "username": "test_user",
            "password": "wrong_password"
        }

        # Send a POST request to the login endpoint
        response = self.app.post('/login', json=login_data)

        # Assert that the response is unauthorized (401)
        self.assertEqual(response.status_code, 401)

        # Assert that the response message indicates incorrect credentials
        self.assertIn('msg', response.json)
        self.assertEqual(response.json['msg'], 'The username or password is incorrect')

        # Clean up the test user
        self.usercollection.delete_one({"username": "test_user"})

    @patch('Authentication.is_mongodb_available')
    def test_mongodb_unavailable(self, mock_mongodb_available):
        # Mock the is_mongodb_available function to return False
        mock_mongodb_available.return_value = False

        # Login data
        login_data = {
            "username": "test_user",
            "password": "test_password"
        }

        # Send a POST request to the login endpoint
        response = self.app.post('/login', json=login_data)

        # Assert that the response indicates database unavailability (504)
        self.assertEqual(response.status_code, 504)

        # Assert that the response message indicates database issues
        self.assertIn('msg', response.json)
        self.assertEqual(response.json['msg'], 'The database is down!!!')

    @patch('Authentication.is_mongodb_available')
    
    def test_session_creation_on_successful_login(self, mock_mongodb_available):
            # Sample data for testing
        sample_user = {
            "username": "test_user",
            "password": "test_password"
        }
        sample_login_data = {
            "username": sample_user["username"],
            "password": sample_user["password"]
        }
        # Mock the is_mongodb_available function to return True
        mock_mongodb_available.return_value = True

        # Create a test user in the database
        usercollection.insert_one(sample_user)

        # Send a POST request to the login endpoint
        response = self.client.post('/login', json=sample_login_data)

        # Assert successful login and session creation
        self.assertEqual(response.status_code, 202)
        self.assertIn('username', response.json)
        self.assertEqual(response.json['username'], sample_user['username'])

        # Access a protected route (replace with actual protected route)
        protected_response = self.client.get('/protected_route')

        # Assert access to protected route with session
        self.assertEqual(protected_response.status_code, 200)  # Adjust based on expected response

    def test_session_persistence_across_requests(self, mock_mongodb_available):
        # Sample data for testing
        sample_user = {
            "username": "test_user",
            "password": "test_password"
        }
        sample_login_data = {
            "username": sample_user["username"],
            "password": sample_user["password"]
        }
        # Mock the is_mongodb_available function to return True
        mock_mongodb_available.return_value = True

        # Create a test user in the database
        usercollection.insert_one(sample_user)

        # Send a POST request to the login endpoint (similar to previous test)
        response = self.client.post('/login', json=sample_login_data)
        self.assertEqual(response.status_code, 202)

        # Access a protected route with the same client instance (using the session)
        protected_response = self.client.get('/protected_route')

        # Assert access to protected route with session
        self.assertEqual(protected_response.status_code, 200)  # Adjust based on expected response


    

if __name__ == '__main__':
    unittest.main()