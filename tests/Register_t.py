import unittest
from MainApp import register, usercollection

class RegistrationTest(unittest.TestCase):

    def setUp(self):
        # Clear any existing user data before tests
        usercollection.delete_many({})

    def tearDown(self):
        # Clear any user data created during tests
        usercollection.delete_many({})

    def test_successful_registration(self):
        # Simulate registration request with new user data
        new_user = {"username": "new_user", "password": "new_password"}
        response = register.route('/auth/register')(data=new_user)

        # Assert response status code and message
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['msg'], 'User created successfully')

        # Check if user is actually inserted in the database
        user_data = usercollection.find_one({"username": "new_user"})
        self.assertIsNotNone(user_data)

    def test_duplicate_username(self):
        # Simulate registration request with an existing username
        existing_user = {"username": "existing_user", "password": "existing_password"}
        usercollection.insert_one(existing_user)

        new_user = {"username": "existing_user", "password": "new_password"}
        response = "yee"
