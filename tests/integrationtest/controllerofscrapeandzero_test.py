import json
# from unittest.mock import patch

# Assuming your Flask application is in a file called app.py
from Reqandscrape.requestsender.chatgptreqsender import change_data as reqsender
from Reqandscrape.zeroshotclassify import calculate_the_zeroshot

from Reqandscrape.search_scrape.PWBDscraperAZ import (
    scrape_amazon,
    item_sorting,
    get_asin,
    urlcleaner,
    get_product_detail,
    get_reviews,
)


# Sample data for testing
sample_search_criteria = "find laptops"
sample_user = "test_user"
sample_zeroshot_data = "This is some text for zeroshot classification"

# @patch('Reqandscrape.requestsender.chatgptreqsender.change_data')
def test_success_reqsender(self, mock_reqsender):
        # Mock the return value of reqsender
        # mock_reqsender.return_value = {"response": "mocked response"}
        
        result = reqsender("electric spoon")
        self.assertIsNotNone(result)
        self.assertEqual(result, {"response": "mocked response"})
    
# @patch('Reqandscrape.requestsender.chatgptreqsender.change_data')
def test_unsuccess_reqsender(self, mock_reqsender):
        # Mock the return value of reqsender to be None
        # mock_reqsender.return_value = None
        
        result = reqsender()
        self.assertIsNone(result)

# @patch('Reqandscrape.zeroshotclassify.calculate_the_zeroshot')
def test_success_calculate_zeroshot(self, mock_calculate):
        # Mock the return value of calculate_the_zeroshot
        # mock_calculate.return_value = {"classification": "mocked classification"}
        
        result = calculate_the_zeroshot()
        self.assertIsNotNone(result)
        self.assertEqual(result, {"classification": "mocked classification"})
    
# @patch('Reqandscrape.zeroshotclassify.calculate_the_zeroshot')
def test_unsuccess_calculate_zeroshot(self, mock_calculate):
        # Mock the return value of calculate_the_zeroshot to be None
        # mock_calculate.return_value = None
        
        result = calculate_the_zeroshot()
        self.assertIsNone(result)

import unittest
from io import StringIO
from unittest.mock import mock_open, patch, MagicMock
import json
import re

from bs4 import BeautifulSoup



class TestScrapeAmazon(unittest.TestCase):
    def test_scrape_amazon_with_proxy(self):
        # Mock requests.get with successful response
        response_mock = MagicMock()
        response_mock.status_code = 200
        response_mock.text = """
        <div class="a-size-medium a-spacing-none a-color-base a-text-normal">Product Name</div>
        <span class='a-price-whole'>$12.34</span>
        <span class='a-icon-alt'>4.5 out of 5 stars</span>
        <a class='a-link-normal s-no-outline' href="https://www.amazon.com/dp/B00KZ0WPIU">Product Link</a>
        """
        with patch('requests.get', return_value=response_mock) as mock_get:
            proxy = {'http': 'http://proxy.example.com', 'https': 'https://proxy.example.com'}
            result = scrape_amazon('keyword', 'search_group', proxy=proxy)

            # Assertions for successful scraping with proxy
            self.assertEqual(mock_get.call_count, 2)  # One call for search, one for product details
            self.assertIn('http://proxy.example.com', mock_get.call_args[0][1]['proxies'])
            self.assertIsNotNone(result)
            self.assertIn('product name', result[0])
            self.assertEqual(result[0]['product name'], 'Product Name')
            self.assertEqual(result[0]['price'], '$12.34')
            self.assertEqual(result[0]['rating'], '4.5 out of 5 stars')
            self.assertEqual(result[0]['url'], 'https://www.amazon.com/dp/B00KZ0WPIU')
            self.assertEqual(result[0]['asin'], 'B00KZ0WPIU')
            self.assertIn('details', result[0])
            self.assertEqual(result[0]['details'][0]['description'], 
                             ['Product Name'])  # Adjust this assertion based on get_product_detail() implementation
            self.assertIn('reviews', result[0])
            # Assert review data based on get_reviews() implementation 

    def test_scrape_amazon_no_proxy(self):
        # Mock requests.get with successful response (no proxy)
        response_mock = MagicMock()
        response_mock.status_code = 200
        response_mock.text = """
        <div class="a-size-medium a-spacing-none a-color-base a-text-normal">Product Name</div>
        <span class='a-price-whole'>$12.34</span>
        <span class='a-icon-alt'>4.5 out of 5 stars</span>
        <a class='a-link-normal s-no-outline' href="https://www.amazon.com/dp/B00KZ0WPIU">Product Link</a>
        """
        with patch('requests.get', return_value=response_mock):
            result = scrape_amazon('keyword', 'search_group')

            # Assertions for successful scraping without proxy
            self.assertEqual(result[0]['product name'], 'Product Name')
            self.assertEqual(result[0]['price'], '$12.34')
            self.assertEqual(result[0]['rating'], '4.5 out of 5 stars')
            self.assertEqual(result[0]['url'], 'https://www.amazon.com/dp/B00KZ0WPIU')
            self.assertEqual(result[0]['asin'], 'B00KZ0WPIU')
            self.assertIn('details', result[0])
            self.assertIn('reviews', result[0])
            # Assert review data based on get_reviews() implementation 

    def test_scrape_amazon_empty_search(self):
        # Mock requests.get with empty search results
        response_mock = MagicMock()
        response_mock.status_code = 200
        response_mock.text = ""
        with patch('requests.get', return_value=response_mock):
            result = scrape_amazon('keyword', 'search_group')
            self.assertEqual(result, None)

    def test_scrape_amazon_request_error(self):
        # Mock requests.get with request error
        response_mock = MagicMock()
        response_mock.status_code = 404
        with patch('requests.get', return_value=response_mock):
            result = scrape_amazon('keyword', 'search_group')
            self.assertIsNone(result)

    def test_scrape_amazon_json_load_error(self):
        # Mock json.load with JSONDecodeError
        with patch('json.load', side_effect=json.JSONDecodeError('Invalid JSON', '', 0)):
            result = scrape_amazon('keyword', 'search_group')
            self.assertIsNone(result)

    def test_item_sorting(self):
        # Mock BeautifulSoup and create sample HTML
        mock_soup = MagicMock()
        mock_soup.find_all.return_value = [
            BeautifulSoup('<div class="a-size-medium a-spacing-none a-color-base a-text-normal">Product 1</div>'
                          '<span class="a-price-whole">$10.00</span>'
                          '<span class="a-icon-alt">4.5 out of 5 stars</span>'
                          '<a class="a-link-normal s-no-outline" href="https://www.amazon.com/dp/B00123ABC">Product Link 1</a>', 
                          'html.parser'),
            BeautifulSoup('<div class="a-size-medium a-spacing-none a-color-base a-text-normal">Product 2</div>'
                          '<span class="a-price-whole">$20.00</span>'
                          '<span class="a-icon-alt">4.0 out of 5 stars</span>'
                          '<a class="a-link-normal s-no-outline" href="https://www.amazon.com/dp/B00234DEF">Product Link 2</a>', 
                          'html.parser'),
        ]
        with patch('bs4.BeautifulSoup', return_value=mock_soup):
            item_sorting(mock_soup.find_all.return_value)
            with open('temporary_search_result.json', 'r') as f:
                data = json.load(f)
                self.assertEqual(len(data), 2)
                self.assertEqual(data[0]['product name'], 'Product 1')
                self.assertEqual(data[0]['price'], '$10.00')
                self.assertEqual(data[0]['rating'], '4.5 out of 5 stars')
                self.assertEqual(data[0]['url'], 'https://www.amazon.com/dp/B00123ABC')
                self.assertEqual(data[0]['asin'], 'B00123ABC') 

    def test_get_asin(self):
        # Mock JSON data
        json_data = [
            {'asin': 'B00123ABC'},
            {'asin': 'B00234DEF'},
            {'asin': None},
        ]
        with patch('builtins.open', mock_open(read_data=json.dumps(json_data))):
            self.assertEqual(get_asin(), ['B00123ABC', 'B00234DEF'])

    def test_urlcleaner(self):
        url = 'https://www.amazon.com/dp/B00KZ0WPIU'
        self.assertEqual(urlcleaner(url), 'B00KZ0WPIU')

        invalid_url = 'https://www.amazon.com/invalid-url'
        self.assertIsNone(urlcleaner(invalid_url))

import unittest
from flask import Flask
from Reqandscrape.ScrapeController import search_bp

class ScrapeControllerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up a Flask test app
        cls.app = Flask(__name__)
        cls.app.register_blueprint(search_bp)
        cls.client = cls.app.test_client()

    def test_scrape(self):
        payload = [
            "test_search_term",
            "test_search_group"
        ]
        response = self.client.post('/scrape', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)  # Assuming the scrape_amazon returns a list

    def test_search_criteria_sender(self):
        payload = [
            "test_criteria",
            "test_people"
        ]
        response = self.client.post('/search_criteria', json=payload)
        self.assertEqual(response.status_code, 200)
        # Assuming the endpoint writes a JSON-compatible response
        self.assertIsInstance(response.json, (dict, type(None)))

    def test_zeroshotstuff(self):
        payload = [
            "test_criteria",
            "test_data"
        ]
        response = self.client.post('/critandprod', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, str)  # Assuming the result is a JSON string

    def test_normaldistribution(self):
        response = self.client.post('/nd')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)  # Assuming normal_dist returns a dictionary

if __name__ == '__main__':
    unittest.main()
