import unittest
from flask import Flask, session
from Reqandscrape.ScrapeController import search_bp
from account.Authentication_Controller import auth_bp
from account.Authentication import authentication, register_newuser, resetpassword_check, resetpassword
from unittest.mock import patch

class FlaskAppTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the Flask app for testing
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.secret_key = 'test_secret_key'
        cls.app.register_blueprint(search_bp)
        cls.app.register_blueprint(auth_bp)
        cls.client = cls.app.test_client()

    def setUp(self):
        # Clear session before each test
        with self.app.test_request_context():
            session.clear()

    # ------------------- ScrapeController Tests ------------------- #
    def test_scrape(self):
        payload = ["search_term", "people_group"]
        response = self.client.post('/scrape', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_search_criteria_sender(self):
        payload = ["criteria", "people"]
        response = self.client.post('/search_criteria', json=payload)
        self.assertEqual(response.status_code, 200)

    def test_zeroshotstuff(self):
        payload = ["criteria", "data"]
        response = self.client.post('/critandprod', json=payload)
        self.assertEqual(response.status_code, 200)

    def test_normaldistribution(self):
        response = self.client.post('/nd')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)

    # ------------------- Authentication_Controller Tests ------------------- #
    def test_login_success(self):
        with patch('account.Authentication.authentication', return_value={"username": "testuser"}):
            payload = {"username": "testuser", "password": "testpass"}
            response = self.client.post('/login', json=payload)
            self.assertEqual(response.status_code, 202)
            self.assertIn("username", response.json)

    def test_login_failure(self):
        with patch('account.Authentication.authentication', return_value="Incorrect passwords"):
            payload = {"username": "testuser", "password": "wrongpass"}
            response = self.client.post('/login', json=payload)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], "Incorrect passwords")

    def test_logout(self):
        with self.client:
            self.client.post('/logout')
            self.assertEqual(session, {})

    def test_register_user_success(self):
        with patch('account.Authentication.register_newuser', return_value="User created successfully"):
            payload = {"username": "newuser", "password": "newpass"}
            response = self.client.post('/register', json=payload)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], "User registered successfully")

    def test_register_user_exists(self):
        with patch('account.Authentication.register_newuser', return_value="Username already exists"):
            payload = {"username": "existinguser", "password": "newpass"}
            response = self.client.post('/register', json=payload)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], "Username already exists")

    def test_get_userinfo_success(self):
        with patch('account.Authentication.access_database', return_value={"username": "testuser", "userinfo": "Test Info", "email": "test@test.com", "dateOfbirth": "2000-01-01"}):
            payload = {"username": "testuser"}
            response = self.client.post('/Information', json=payload)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json[0], "testuser")

    def test_get_userinfo_not_found(self):
        with patch('account.Authentication.access_database', return_value=None):
            payload = {"username": "unknownuser"}
            response = self.client.post('/Information', json=payload)
            self.assertEqual(response.status_code, 404)

    def test_reset_password_success(self):
        with patch('account.Authentication.resetpassword', return_value="success"):
            payload = {"username": "testuser", "answer": "correct_answer", "password": "newpass"}
            response = self.client.post('/reset_password', json=payload)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, "success")

    def test_reset_password_failure(self):
        with patch('account.Authentication.resetpassword', return_value="unsuccess"):
            payload = {"username": "testuser", "answer": "wrong_answer", "password": "newpass"}
            response = self.client.post('/reset_password', json=payload)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, "unsuccess")

if __name__ == '__main__':
    unittest.main()
