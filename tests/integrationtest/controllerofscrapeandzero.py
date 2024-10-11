import json
from unittest.mock import patch

# Assuming your Flask application is in a file called app.py
from Reqandscrape.ScrapeController import app, usercollection  # Import relevant parts

# Sample data for testing
sample_search_criteria = "find laptops"
sample_user = "test_user"
sample_zeroshot_data = "This is some text for zeroshot classification"


def test_search_criteria_sender():
    # Mock the receiveinput function
    with patch("Reqandscrape.requestsender.chatgptreqsender.receiveinput") as mock_receiveinput:
        mock_receiveinput.return_value = "Mocked response from receiveinput"

        # Create a test client
        with app.test_client() as client:
            # Prepare JSON data
            data = json.dumps({"username": sample_user, "criteria": sample_search_criteria})

            # Send POST request
            response = client.post("/search_criteria", data=data, content_type="application/json")

            # Assert status code and response data
            assert response.status_code == 200
            assert json.loads(response.data) == "Mocked response from receiveinput"

            # Mock session for user collection interaction
            session = {"username": sample_user}
            with patch.object(usercollection, "find") as mock_find, patch.object(usercollection, "insert") as mock_insert:
                # Simulate session existence
                mock_find.return_value = True

                # Send another request with mocked session
                response = client.post("/search_criteria", data=data, content_type="application/json")

                # Assert data is inserted into the collection
                mock_insert.assert_called_once_with({"criteria": "Mocked response from receiveinput"})


def test_search_criteria_test_sender():
    # Create a test client
    with app.test_client() as client:

        # Send POST request
        response = client.post("/search_criteria_test", content_type="application/json")

        # Assert status code and response data (replace with expected mock data)
        assert response.status_code == 200
        assert json.loads(response.data) == "Mocked response from receiveinputtest"  # Adjust with expected data


def test_search_prod_sender_test():
    # Create a test client
    with app.test_client() as client:

        # Send POST request
        response = client.post("/search_prod_test", content_type="application/json")

        # Assert status code and response data (replace with expected mock data)
        assert response.status_code == 200
        assert json.loads(response.data) == {"data": "This is mocked data from json_data_mock"}  # Adjust with expected data


def test_scrape_test():
    # Create a test client
    with app.test_client() as client:

        # Send POST request
        response = client.post("/scrape_test", content_type="application/json")

        # Assert status code and response data (replace with expected mock data)
        assert response.status_code == 200
        assert json.loads(response.data) == {"data": "This is mocked data from json_data_mock"}  # Adjust with expected data


def test_zeroshotstuff_test():
    # Create a test client
    with app.test_client() as client:

        # Send POST request
        response = client.post("/critandprod_test", content_type="application/json")

        # Assert status code and response data (replace with expected mock data)
        assert response.status_code == 200
        assert json.loads(response.data) == "Mocked response from calculate_the_zeroshot_test"  # Adjust with expected data