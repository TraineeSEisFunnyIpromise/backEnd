import pytest
from database.databasemanager import (
    access_database,
    delete_user,
    update_user_aboutme,
    update_password,
    add_new_user,
    check_username,
    check_database_status,
    write_to_database_by_name,
)


class TestDatabaseManager:
    def setup_method(self):
        self.username = 'test1'
        self.password = '1234'
        self.user_data = {
            'name': 'test1',
            'password': '1234',
            'about me': 'ye',
            'question for reset password': 'slurpy',
            'answer for reset password': 'slurp',
            'email': 'something@gmail.com',
            'dateofbirth': '2001-05'
        }

    def test_access_database(self):
        # Assuming access_database returns a dictionary with user data
        result = access_database(self.username)
        assert result == self.user_data  # Assert against expected data

    def test_check_database_status_success(self):
        assert check_database_status() == True  # Call the function directly

    def test_check_database_status_failure(self):
        # Simulate potential errors (replace with appropriate exception handling)
        with pytest.raises(Exception):
            check_database_status()  # Expect an exception

    def test_check_username_success(self):
        assert check_username(self.username) == True  # Call the function

    def test_check_username_failure(self):
        assert check_username('someuitaoiui') == False  # Call the function

    def test_write_to_database_by_name_success(self):
        # Simulate successful update (replace with actual update logic)
        assert write_to_database_by_name(self.username, {'data': 'test'}) == True

    def test_write_to_database_by_name_failure(self):
        # Simulate failed update (replace with actual update logic)
        assert write_to_database_by_name(self.username, {'data': 'test'}) == False

    def test_update_user_aboutme_success(self):
        # Simulate successful update (replace with actual update logic)
        assert update_user_aboutme(self.username, 'new about me') == True

    def test_update_user_aboutme_failure(self):
        # Simulate failed update (replace with actual update logic)
        assert update_user_aboutme(self.username, 'new about me') == False

    def test_update_password_success(self):
        # Simulate successful update (replace with actual update logic)
        assert update_password(self.username, 'newpassword') == True

    def test_update_password_failure(self):
        # Simulate failed update (replace with actual update logic)
        assert update_password(self.username, 'newpassword') == False

    def test_add_new_user_success(self):
        # Simulate successful insert (replace with actual insert logic)
        assert add_new_user(self.username, self.user_data) == True

    def test_add_new_user_failure(self):
        # Simulate failed insert (replace with actual error handling)
        with pytest.raises(Exception):
            add_new_user(self.username, self.user_data)

    def test_delete_user_success(self):
        # Simulate successful delete (replace with actual delete logic)
        assert delete_user(self.username) == True

    def test_delete_user_failure(self):
        # Simulate failed delete (replace with actual error handling)
        with pytest.raises(Exception):
            delete_user(self.username)