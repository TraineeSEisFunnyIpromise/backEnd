import unittest
from MainApp import app
from account.userinfo import update_oldpassword,update_aboutme,delete_account
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['Database1']
usercollection = db['db1']

class TestUserInfo(unittest.TestCase):


    def setUp(self):
        self.app = app.test_client()
        self.user_data = {'name': 'Test1','password': '1234', 'About me':'ye', 'Question for reset password':'slurpy', 
'Answer for reset password':'slurp'}
        self.testaboutme = "yes"
        self.password="1234"

    
    def test_success_update_oldpassword(self):
        username = 'test1'
        newpassword = "1234567"
        result = update_oldpassword(username,newpassword)
        self.assertIsNotNone(result)

    def test_unsuccess_update_oldpassword(self):
        username = ''
        newpassword = "1234567"
        result = update_oldpassword(username,newpassword)
        self.assertIsNone(result)

    def test_success_update_aboutme(self):
        username = 'test1'
        testaboutme = "yes"
        result = update_aboutme(username,testaboutme)
        self.assertIsNotNone(result)
    
    def test_unsuccess_update_aboutme(self):
        username = ''
        testaboutme = "yes"
        result = update_aboutme(username,testaboutme)
        self.assertIsNone(result)
    
    def test_success_delete_account(self):
        username = 'test1'
        password="1234"
        result = delete_account(username,password)
        self.assertIsNotNone(result)
    
    def test_unsuccess_delete_account(self):
        username = 'test1'
        password=""
        result = delete_account(username,password)
        self.assertIsNone(result)


    def test_information_success(self):
        response = self.app.post('/userinfo/Information')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['profile'], self.user_data)

    def test_information_no_session(self):
        # Simulate no username in session
        with self.app.session_transaction() as session:
            session.pop('username', None)

        response = self.app.post('/userinfo/Information')
        self.assertEqual(response.status_code, 401)  # Expect unauthorized without session

if __name__ == '__main__':
    unittest.main()
