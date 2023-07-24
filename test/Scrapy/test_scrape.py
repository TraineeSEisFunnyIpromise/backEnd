import unittest
from Flask_login import some_function_to_test

class TestApp(unittest.TestCase):
	def test_Scraped_Data_FB(self):
		# Test case for some_function_to_test
		result = some_function_to_test(3, 5)
		self.assertEqual(result, 8)
		
	def test_Scraped_ID_FB(self):
		# Test case for some_function_to_test
		result = some_function_to_test(3, 5)
		self.assertEqual(result, 8)

if __name__ == '__main__':
    unittest.main()