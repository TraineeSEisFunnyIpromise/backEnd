import unittest
from unittest.mock import AsyncMock
from Reqandscrape.zeroshotclassify import calculate_the_zeroshot
# Import your functions


class TestCalculateZeroshot(unittest.TestCase):
    def test_calculate_zeroshot(self):
        # Sample input data
        input_texts = ["This is a sample text about technology.", "This is another sample text about fashion."]
        dynamic_labels = ["Technology", "Fashion", "Health"]

        # Call the function
        result = calculate_the_zeroshot(input_texts, dynamic_labels)

        # Assert that the output is not empty
        self.assertIsNotNone(result)
        self.assertGreater(len(result["data"]), 0)

if __name__ == '__main__':
    unittest.main()