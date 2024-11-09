import unittest
from unittest.mock import patch, AsyncMock
import asyncio

# Import your functions
from Reqandscrape.search_scrape.PWBDscraperAZ import search_review

class TestSearchReview(unittest.TestCase):

    def test_search_review_test(self):
        # Arrange (set up test data)
        input_a = "electric fan"
        input_b = "student"

        # Act (call the function)
        result = search_review(input_a, input_b)

        # Assert (verify the expected outcome)
        self.assertEqual(result, True)  # Expected to return the defined string

    def test_success_scrape_product():
        product_url = ""
    
    def test_unsuccess_scrape_product():
        product_url = ""
    
    def url_cleaner():
        print()
    
    def test_success_get_asin():
        print()

    def test_unsuccess_get_asin():
        print()

if __name__ == '__main__':
    unittest.main()
                        
