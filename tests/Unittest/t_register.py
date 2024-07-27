import unittest
from MainApp import app
from account.userinfo import userinformation_bp
from pymongo import MongoClient  # For mocking (optional)

class TestUserInfo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Optional: Mock the MongoClient to isolate endpoint logic
        cls.mock_client = unittest.mock.Mock(MongoClient)
        cls.mock_db = cls.mock_client.return_value.Database1
        cls.mock_collection = cls.mock_db.return_value.DB1

        # Patch MongoClient in the app (optional)
        with unittest.mock.patch('app.MongoClient', return_value=cls.mock_client):
            app.config['TESTING'] = True  # Enable testing mode

    @classmethod
    def tearDownClass(cls):
        app.config['TESTING'] = False  # Disable testing mode

    def setUp(self):
        self.app = app.test_client()
        self.username = 'test1'
        self.user_data = {'name': 'Test1','password': '1234', 'About me':'ye', 'Question for reset password':'slurpy', 
'Answer for reset password':'slurp'}

        # Simulate a session with the username (optional)
        with self.app.session_transaction() as session:
            session['username'] = self.username

        # Mock the database collection behavior (optional)
        self.mock_collection.find_one.return_value = self.user_data.copy()

    def test_sessioncheck_success(self):
        # Refer to the previous test for explanation
        response = self.app.post('/userinfo/Sessioncheck')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'test_user', response.data)  # Assert username is present

    def test_information_success(self):
        response = self.app.post('/userinfo/Information')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['profile'], self.user_data)

        # Additional assertions (optional)
        # You can assert specific keys or values in the returned profile data

    def test_information_no_session(self):
        # Simulate no username in session
        with self.app.session_transaction() as session:
            session.pop('username', None)

        response = self.app.post('/userinfo/Information')
        self.assertEqual(response.status_code, 401)  # Expect unauthorized without session

if __name__ == '__main__':
    unittest.main()
