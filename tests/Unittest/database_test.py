from unittest.mock import patch, MagicMock
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

@patch('database.databasemanager.usercollection')
def test_access_database(mock_usercollection):
    mock_usercollection.find_one.return_value = {'username': 'testuser', 'about me': 'test'}
    result = access_database('testuser')
    assert result == {'username': 'testuser', 'about me': 'test'}

@patch('database.databasemanager.client')
def test_check_database_status_success(mock_client):
    mock_client.server_info.return_value = {}
    assert check_database_status() == True

@patch('database.databasemanager.client')
def test_check_database_status_failure(mock_client):
    mock_client.server_info.side_effect = Exception('Connection error')
    assert check_database_status() == False

@patch('database.databasemanager.usercollection')
def test_check_username_success(mock_usercollection):
    mock_usercollection.find_one.return_value = {'username': 'testuser'}
    assert check_username('testuser') == True

@patch('database.databasemanager.usercollection')
def test_check_username_failure(mock_usercollection):
    mock_usercollection.find_one.return_value = None
    assert check_username('someuitaoiui') == False

@patch('database.databasemanager.usercollection')
def test_write_to_database_by_name_success(mock_usercollection):
    mock_usercollection.update_one.return_value.modified_count = 1
    assert write_to_database_by_name('testuser', {'data': 'test'}) == True

@patch('database.databasemanager.usercollection')
def test_write_to_database_by_name_failure(mock_usercollection):
    mock_usercollection.update_one.return_value.modified_count = 0
    assert write_to_database_by_name('testuser', {'data': 'test'}) == False

@patch('database.databasemanager.usercollection')
def test_update_user_aboutme_success(mock_usercollection):
    mock_usercollection.update_one.return_value.modified_count = 1
    assert update_user_aboutme('testuser', 'new about me') == True

@patch('database.databasemanager.usercollection')
def test_update_user_aboutme_failure(mock_usercollection):
    mock_usercollection.update_one.return_value.modified_count = 0
    assert update_user_aboutme('testuser', 'new about me') == False

@patch('database.databasemanager.usercollection')
def test_update_password_success(mock_usercollection):
    mock_usercollection.update_one.return_value.modified_count = 1
    assert update_password('testuser', 'newpassword') == True

@patch('database.databasemanager.usercollection')
def test_update_password_failure(mock_usercollection):
    mock_usercollection.update_one.return_value.modified_count = 0
    assert update_password('testuser', 'newpassword') == False

@patch('database.databasemanager.usercollection')
def test_add_new_user_success(mock_usercollection):
    mock_usercollection.insert_one.return_value.inserted_id = 'someid'
    assert add_new_user('testuser', {'username': 'testuser'}) == True

@patch('database.databasemanager.usercollection')
def test_add_new_user_failure(mock_usercollection):
    mock_usercollection.insert_one.side_effect = Exception('Insert error')
    assert add_new_user('testuser', {'username': 'testuser'}) == False

@patch('database.databasemanager.usercollection')
def test_delete_user_success(mock_usercollection):
    mock_usercollection.delete_one.return_value.deleted_count = 1
    assert delete_user('testuser') == True

@patch('database.databasemanager.usercollection')
def test_delete_user_failure(mock_usercollection):
    mock_usercollection.delete_one.return_value.deleted_count = 0
    assert delete_user('testuser') == False