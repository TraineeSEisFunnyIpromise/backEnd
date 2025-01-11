import unittest
from unittest.mock import patch, MagicMock
from Reqandscrape.zeroshotclassify import calculate_the_zeroshot, classify_and_sum_scores

class TestCalculateZeroshot(unittest.TestCase):

    @patch('Reqandscrape.zeroshotclassify.pipeline')
    def test_calculate_zeroshot(self, mock_pipeline):
        # Mock the classifier
        mock_classifier = MagicMock()
        mock_classifier.return_value = {
            'labels': ['Technology', 'Fashion', 'Health'],
            'scores': [0.9, 0.05, 0.05]
        }
        mock_pipeline.return_value = mock_classifier

        # Sample input data
        input_texts = ["This is a sample text about technology.", "This is another sample text about fashion."]
        dynamic_labels = ["Technology", "Fashion", "Health"]

        # Call the function
        result = calculate_the_zeroshot(input_texts, dynamic_labels)

        # Assert that the output is not empty
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)
        self.assertEqual(result[0]['Label'], 'Technology')
        self.assertAlmostEqual(result[0]['Score'], 0.45, places=2)

    @patch('Reqandscrape.zeroshotclassify.pipeline')
    def test_classify_and_sum_scores(self, mock_pipeline):
        # Mock the classifier
        mock_classifier = MagicMock()
        mock_classifier.return_value = {
            'labels': ['Technology', 'Fashion', 'Health'],
            'scores': [0.9, 0.05, 0.05]
        }
        mock_pipeline.return_value = mock_classifier

        # Sample input data
        input_texts = ["This is a sample text about technology.", "This is another sample text about fashion."]
        input_labels = ["Technology", "Fashion", "Health"]

        # Call the function
        result = classify_and_sum_scores(input_texts, input_labels)

        # Assert that the output is correct
        self.assertIsNotNone(result)
        self.assertEqual(result['Technology'], 1.8)
        self.assertEqual(result['Fashion'], 0.1)
        self.assertEqual(result['Health'], 0.1)

if __name__ == '__main__':
    unittest.main()