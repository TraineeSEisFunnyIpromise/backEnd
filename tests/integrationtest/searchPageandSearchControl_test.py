import unittest
# from unittest.mock import patch, AsyncMock


# Import your functions
from Reqandscrape.search_scrape.PWBDscraperAZ import scrape_amazon, scrape_amazon_product
from Reqandscrape.requestsender.chatgptreqsender import change_data as reqsender


class TestSearchReview(unittest.TestCase):
                
        asin = ["DP023543", "DP546503", "DP003156"]
        url = ["", "", ""]
        word = "electric car"

        @classmethod
        def setUpClass(cls):
                cls.soup = open("raw_result_test.txt", "w+", encoding="utf-8")

        @classmethod
        def tearDownClass(cls):
                cls.soup.close()

        def test_success_scrape_product(self):
                result = scrape_amazon_product(self.asin)
                self.assertIsNotNone(result)
        
        def test_unsuccess_scrape_product(self):
                result = scrape_amazon_product("")
                self.assertIsNone(result)

        def test_success_change_data(self):
                result = reqsender(self.word)
                self.assertIsNotNone(result)
        
        def test_unsuccess_change_data(self):
                result = reqsender("")
                self.assertIsNone(result)

        def test_scrape_amazon_invalid_data_type(self):
                with self.assertRaises(TypeError):
                        scrape_amazon(12345, None)

        # @patch('Reqandscrape.search_scrape.PWBDscraperAZ.requests.get')
        def test_scrape_amazon_product_network_error(self, mock_get):
                # mock_get.side_effect = Exception("Network error")
                result = scrape_amazon_product(self.asin)
                self.assertIsNone(result)

if __name__ == '__main__':
        unittest.main()