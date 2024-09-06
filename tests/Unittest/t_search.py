import unittest
from unittest.mock import patch, AsyncMock
import asyncio

# Import your functions
from Reqandscrape.Search_scrape.PWBDscraperAZ import search_review

class TestSearchReview(unittest.TestCase):

    def test_search_review_test(self):
        # Arrange (set up test data)
        input_a = "electric fan"
        input_b = "student"

        # Act (call the function)
        result = search_review(input_a, input_b)

        # Assert (verify the expected outcome)
        self.assertEqual(result, True)  # Expected to return the defined string

if __name__ == '__main__':
    unittest.main()
                        
