from account.Authentication import login

class testlogin:
    def test_login(self):
        tests_username = ""
        tests_password = ""
        assert login(test_username,test_password)