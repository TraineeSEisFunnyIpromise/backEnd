import unittest

from Reqandscrape.zeroshotclassify import calculate_the_zeroshot, classify_and_sum_scores
from Reqandscrape.NDcalculate import normal_dist
import unittest
import json
import numpy as np
from io import StringIO  # For mocking file I/O

class TestCalculateZeroshot(unittest.TestCase):

    # @patch('Reqandscrape.zeroshotclassify.pipeline')
    def test_calculate_zeroshot(self, mock_pipeline):
        # Mock the classifier
        # mock_classifier = MagicMock()
        # mock_classifier.return_value = {
        #     'labels': ['Technology', 'Fashion', 'Health'],
        #     'scores': [0.9, 0.05, 0.05]
        # }
        # mock_pipeline.return_value = mock_classifier

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

    # @patch('Reqandscrape.zeroshotclassify.pipeline')
    def test_classify_and_sum_scores(self, mock_pipeline):
        # Mock the classifier
        # mock_classifier = MagicMock()
        # mock_classifier.return_value = {
        #     'labels': ['Technology', 'Fashion', 'Health'],
        #     'scores': [0.9, 0.05, 0.05]
        # }
        # mock_pipeline.return_value = mock_classifier

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

    def test_ND(self, mock_pipeline):
        # Mock the classifier
        # mock_classifier = MagicMock()
        # mock_classifier.return_value = {
        #     'labels': ['Technology', 'Fashion', 'Health'],
        #     'scores': [0.9, 0.05, 0.05]
        # }
        # mock_pipeline.return_value = mock_classifier

        # Sample input data
        result = normal_dist()
        self.assertIsNotNone(result)

        # Assert that the output is not emp
    def test_empty_json(self):
        # Mock an empty JSON file
        empty_json_content = ""
        with unittest.mock.patch('builtins.open', return_value=StringIO(empty_json_content)) as mock_file:
            result = normal_dist()
            self.assertIsNone(result)
            mock_file.assert_called_once_with('temporary_search_result.json', 'r', encoding='utf-8')

    def test_invalid_json(self):
        # Mock invalid JSON content
        invalid_json_content = "This is not valid JSON"
        with unittest.mock.patch('builtins.open', return_value=StringIO(invalid_json_content)) as mock_file, \
             unittest.mock.patch('json.loads') as mock_loads:
            mock_loads.side_effect = json.JSONDecodeError("Invalid JSON", invalid_json_content, 0)
            result = normal_dist()
            self.assertIsNone(result)
            mock_file.assert_called_once_with('temporary_search_result.json', 'r', encoding='utf-8')
            mock_loads.assert_called_once_with(invalid_json_content)

    def test_empty_json_list(self):
        # Mock an empty JSON list
        empty_json_list = "[]"
        with unittest.mock.patch('builtins.open', return_value=StringIO(empty_json_list)) as mock_file:
            result = normal_dist()
            self.assertIsNone(result)
            mock_file.assert_called_once_with('temporary_search_result.json', 'r', encoding='utf-8')

    def test_non_dictionary_first_item(self):
        # Mock a JSON list with a non-dictionary first item
        non_dict_json = "[1, 2, 3]"
        with unittest.mock.patch('builtins.open', return_value=StringIO(non_dict_json)) as mock_file:
            with self.assertRaises(TypeError):
                normal_dist()
            mock_file.assert_called_once_with('temporary_search_result.json', 'r', encoding='utf-8')

    def test_valid_json(self):
        # Mock valid JSON data with prices
        valid_json_data = '[{"price": "$12.34"}, {"price": "$56.78"}]'
        with unittest.mock.patch('builtins.open', return_value=StringIO(valid_json_data)) as mock_file, \
             unittest.mock.patch('numpy.std') as mock_std, \
             unittest.mock.patch('numpy.mean') as mock_mean:
            mock_std.return_value = 10
            mock_mean.return_value = 30
            result = normal_dist()
            self.assertEqual(result, [2, 10, 30, 2271])
            mock_file.assert_called_once_with('temporary_search_result.json', 'r', encoding='utf-8')
            mock_std.assert_called_once_with([1234, 5678])
            mock_mean.assert_called_once_with([1234, 5678])

    def test_valid_json_no_prices(self):
        # Mock valid JSON data without prices
        valid_json_no_prices = '[{"name": "Item A"}, {"name": "Item B"}]'
        with unittest.mock.patch('builtins.open', return_value=StringIO(valid_json_no_prices)) as mock_file:
            result = normal_dist()
            self.assertEqual(result, [])
            mock_file.assert_called_once_with('temporary_search_result.json', 'r', encoding='utf-8')



if __name__ == '__main__':
    unittest.main()