import unittest
from unittest.mock import patch, AsyncMock

# Import your functions
from Reqandscrape.search_scrape.PWBDscraperAZ import scrape_amazon,scrape_amazon_product
from Reqandscrape.requestsender.chatgptreqsender import change_data as reqsender


class TestSearchReview(unittest.TestCase):
    
    asin = ["DP023543","DP546503","DP003156"]
    url = ["","",""]
    soup = open("raw_result_test.txt", "w+",encoding="utf-8")
    word = "electric car"
    
def test_success_scrape_product(self):
        for asin in self.asin:
            result = scrape_amazon_product(asin)
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

def test_scrape_amazon_product_invalid_data_type(self):
        with self.assertRaises(TypeError):
            scrape_amazon_product(12345)

def test_change_data_invalid_data_type(self):
        with self.assertRaises(TypeError):
            reqsender(12345)

def test_scrape_amazon_empty_search_group(self):
        result = scrape_amazon("electric spoon", None)
        self.assertIsNotNone(result)

def test_scrape_amazon_product_empty_json_file(self):
        result = scrape_amazon_product("DP023543", None)
        self.assertIsNotNone(result)

def test_change_data_empty_word(self):
        result = reqsender(None)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
                        
