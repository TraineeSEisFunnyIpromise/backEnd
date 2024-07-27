import unittest
from unittest.mock import AsyncMock
from comparesys.CompareController import compare_test
# Import your functions
from reqandscrape.scrape.PWRAZscrape import extract_review_title, extract_review_body, extract_product_colour, extract_rating

class TestReviewExtraction(unittest.TestCase):

    async def test_compare(self):
        # Mock review element with title
        review_element = AsyncMock()
        review_element.evaluate.return_value = "This is a great product!"

        title = await extract_review_title(review_element)

        # Assert the extracted title is correct (modify based on your logic)
        self.assertEqual(title, "This is a great product!")