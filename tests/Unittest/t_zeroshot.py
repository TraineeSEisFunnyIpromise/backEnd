import unittest
from unittest.mock import AsyncMock
from Reqandscrape.zeroshotclassify import calculate_the_zeroshot_test
# Import your functions


class TestReviewExtraction(unittest.TestCase):

    async def test_compare(self):
        title = await calculate_the_zeroshot_test()

        # Assert the extracted title is correct (modify based on your logic)
        self.assertEqual(title, "This is a great product!")