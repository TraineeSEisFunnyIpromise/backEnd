import unittest
# from unittest.mock import patch, MagicMock
from account.Authentication import authentication, register_newuser, resetpassword

class TestLoginEndpoint(unittest.TestCase):

    def setUp(self):
        self.username = 'test1'
        self.password = '1234'
        self.user_data = {'name': 'test1',
                          'password': '1234',
                          'about me':'ye', 
                          'question for reset password':'slurpy', 
                          'answer for reset password':'slurp',
                          'email':'something@gmail.com',
                          'dateofbirth':'2001-05'
                          }

    # @patch('account.Authentication.check_database_status', return_value=True)
    # @patch('account.Authentication.check_username', return_value=True)
    # @patch('account.Authentication.access_database', return_value=None)
    def test_successful_authentication(self, mock_check_db_status, mock_check_username, mock_access_db):
        result = authentication(self.username, self.password)
        self.assertIsNotNone(result)
        self.assertEqual(result['username'], self.username)

    # @patch('account.Authentication.check_database_status', return_value=True)
    # @patch('account.Authentication.check_username', return_value=False)
    def test_user_not_found(self, mock_check_db_status, mock_check_username):
        result = authentication(self.username, self.password)
        self.assertEqual(result, 'user not found')

    # @patch('account.Authentication.check_database_status', return_value=False)
    def test_server_down(self, mock_check_db_status):
        result = authentication(self.username, self.password)
        self.assertEqual(result, 'The server is down')

    # @patch('account.Authentication.check_database_status', return_value=True)
    # @patch('account.Authentication.check_username', return_value=True)
    # @patch('account.Authentication.access_database', return_value={'password': 'wrongpassword'})
    def test_incorrect_password(self, mock_check_db_status, mock_check_username, mock_access_db):
        result = authentication(self.username, 'wrongpassword')
        self.assertEqual(result, 'Incorrect passwords')

    # @patch('account.Authentication.access_database', return_value=None)
    # @patch('account.Authentication.update_password', return_value=None)
    def test_successful_reset_password(self, mock_access_db, mock_update_password):
        result = resetpassword(self.username, 'answer', 'newpassword')
        self.assertEqual(result, 'success')

    # @patch('account.Authentication.access_database', return_value=None)
    def test_unsuccessful_reset_password(self, mock_access_db):
        result = resetpassword(self.username, 'wronganswer', 'newpassword')
        self.assertEqual(result, 'unsuccess')

    # @patch('account.Authentication.check_username', return_value=False)
    # @patch('account.Authentication.add_new_user', return_value=None)
    def test_successful_register_newuser(self, mock_check_username, mock_add_new_user):
        result = register_newuser(self.user_data)
        self.assertEqual(result, 'User created successfully')

    # @patch('account.Authentication.check_username', return_value=True)
    def test_username_already_exists(self, mock_check_username):
        result = register_newuser(self.user_data)
        self.assertEqual(result, 'Username already exists')



if __name__ == '__main__':
    unittest.main()
