import unittest
from flask import Flask, session
from account.userinfo_Controller import userinformation_bp
from account.userinfo import update_oldpassword, update_aboutme, delete_account
from unittest.mock import patch
from datetime import datetime

class TestUserInfo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.secret_key = 'test_secret_key'
        cls.app.register_blueprint(userinformation_bp)
        cls.client = cls.app.test_client()

    def setUp(self):
        with self.app.test_request_context():
            session.clear()

    # ------------------- Test Routes ------------------- #
    @patch('account.userinfo.update_aboutme', return_value="Update successful")
    def test_update_success(self, mock_update):
        payload = {"username": "testuser", "aboutme": "New about me"}
        response = self.client.post('/Update', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "Update successful")

    @patch('account.userinfo.update_aboutme', return_value="Update failed")
    def test_update_failure(self, mock_update):
        payload = {"username": "testuser", "aboutme": "New about me"}
        response = self.client.post('/Update', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "Update failed")

    @patch('account.userinfo.access_database', return_value={"username": "testuser", "password": "password123"})
    @patch('account.userinfo.delete_user', return_value=True)
    def test_delete_account_success(self, mock_delete, mock_access):
        payload = {"username": "testuser", "password": "password123"}
        response = self.client.post('/Delete', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['msg'], "remove successful")

    @patch('account.userinfo.access_database', return_value={"username": "testuser", "password": "password123"})
    def test_delete_account_wrong_password(self, mock_access):
        payload = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post('/Delete', json=payload)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['msg'], "remove unsuccessful")

    @patch('account.userinfo.update_oldpassword', return_value="Password updated successfully")
    def test_update_password_success(self, mock_update_password):
        payload = {"username": "testuser", "password": "newpassword123"}
        response = self.client.post('/PasswordUpdate', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, "Password updated successfully")

    @patch('account.userinfo.update_oldpassword', return_value="Password updated successfully")
    def test_update_password_failure(self, mock_update_password):
        payload = {"username": "", "password": "newpassword123"}
        response = self.client.post('/PasswordUpdate', json=payload)
        self.assertEqual(response.status_code, 400)

    # ------------------- Test Logic Functions ------------------- #
    @patch('database.databasemanager.update_user_aboutme', return_value=True)
    def test_update_aboutme_success(self, mock_db_update):
        result = update_aboutme("testuser", "Updated about me")
        self.assertEqual(result, "update success")

    @patch('database.databasemanager.update_user_aboutme', return_value=False)
    def test_update_aboutme_failure(self, mock_db_update):
        result = update_aboutme("testuser", "Updated about me")
        self.assertEqual(result, "update unsuccess")

    @patch('database.databasemanager.update_password', return_value=True)
    def test_update_oldpassword_success(self, mock_db_update):
        result = update_oldpassword("testuser", "newpassword123")
        self.assertEqual(result, "Reset password successful")

    @patch('database.databasemanager.update_password', return_value=False)
    def test_update_oldpassword_failure(self, mock_db_update):
        result = update_oldpassword("testuser", "newpassword123")
        self.assertEqual(result, "Reset password unsuccessful")

    @patch('database.databasemanager.check_username', return_value=True)
    @patch('database.databasemanager.delete_user', return_value=True)
    def test_delete_account_logic_success(self, mock_delete, mock_check_username):
        result, success = delete_account("testuser")
        self.assertTrue(success)
        self.assertEqual(result.json['msg'], "remove succesful")

    @patch('database.databasemanager.check_username', return_value=False)
    def test_delete_account_logic_failure(self, mock_check_username):
        result, success = delete_account("unknownuser")
        self.assertFalse(success)
        self.assertEqual(result.json['msg'], "user not found")

if __name__ == '__main__':
    unittest.main()