import unittest
from unittest.mock import AsyncMock

# Import your functions
from reqandscrape.scrape.PWRAZscrape import extract_review_title, extract_review_body, extract_product_colour, extract_rating

class TestReviewExtraction(unittest.TestCase):

    async def test_extract_review_title_with_text(self):
        # Mock review element with title
        review_element = AsyncMock()
        review_element.evaluate.return_value = "This is a great product!"

        title = await extract_review_title(review_element)

        # Assert the extracted title is correct (modify based on your logic)
        self.assertEqual(title, "This is a great product!")

    async def test_extract_review_title_no_text(self):
        # Mock review element without title
        review_element = AsyncMock()
        review_element.evaluate.return_value = ""

        title = await extract_review_title(review_element)

        # Assert the title is handled correctly if no text is found
        self.assertEqual(title, "Not Available")  # Adjust default value if needed)


    async def test_extract_review_title_no_text(self):
        # Mock review element without title
        review_element = AsyncMock()
        review_element.evaluate.return_value = ""

        title = await extract_review_title(review_element)
        self.assertEqual(title, "not available")

    # Similar tests for extract_review_body, extract_product_colour, and extract_rating