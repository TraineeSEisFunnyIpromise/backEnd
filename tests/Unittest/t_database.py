
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client['Database1']
usercollection = db['db1']

from unittest.mock import patch, Mock

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

@patch('database.databasemanager.MongoClient')
def test_access_database(mock_usercollection):
    mock_usercollection.find_one.return_value = {'username': 'testuser', 'about me': 'test'}
    result = access_database('testuser')
    assert result == {'username': 'testuser', 'about me': 'test'}



@patch('database.databasemanager.MongoClient')
def test_check_database_status_success(mock_client):
    mock_client.return_value.server_info.return_value = {}
    assert check_database_status() == True

@patch('database.databasemanager.MongoClient')
def test_check_database_status_failure(mock_client):
    mock_client.side_effect = Exception('Connection error')
    assert check_database_status() == False

@patch('database.databasemanager.MongoClient')
def test_check_username_success(mock_client):

    assert check_username() == True

@patch('database.databasemanager.MongoClient')
def test_check_username_failure(mock_client):
    
    assert check_username() == False

@patch('database.databasemanager.MongoClient')
def test_check_database_status_success(mock_client):

    assert write_to_database_by_name() == True

@patch('database.databasemanager.MongoClient')
def test_check_database_status_failure(mock_client):

    assert write_to_database_by_name() == False

@patch('database.databasemanager.MongoClient')
def test_update_user_aboutme_success(mock_client):

    assert update_user_aboutme() == True

@patch('database.databasemanager.MongoClient')
def test_update_user_aboutme_failure(mock_client):

    assert update_user_aboutme() == False

@patch('database.databasemanager.MongoClient')
def test_update_password_success(mock_client):

    assert update_password() == True

@patch('database.databasemanager.MongoClient')
def test_update_password_failure(mock_client):

    assert update_password() == False


@patch('database.databasemanager.MongoClient')
def test_add_new_user_success(mock_client):

    assert add_new_user() == True

@patch('database.databasemanager.MongoClient')
def test_add_new_user_failure(mock_client):

    assert add_new_user() == False


@patch('database.databasemanager.MongoClient')
def test_delete_user_success(mock_client):

    assert delete_user() == True

@patch('database.databasemanager.MongoClient')
def test_delete_user_failure(mock_client):

    assert delete_user() == False

