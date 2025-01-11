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
    
    def test_success_search_product(self):
        result = scrape_amazon("electric spoon","")
        self.assertIsNotNone(result)
    
    def test_unsuccess_search_product(self):
        result = scrape_amazon("electric spoon","")
        self.assertIsNone(result)
        
    def test_success_scrape_product(self,asin):
        result = scrape_amazon_product(asin)
        self.assertIsNotNone(result)
    
    def test_unsuccess_scrape_product(self):
        result = scrape_amazon_product([])
        self.assertIsNone(result)

    def test_success_scrape_product(self,word):
        result = reqsender(word)
        self.assertIsNotNone(result)
    
    def test_unsuccess_scrape_product(self):
        result = reqsender([])
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
                        
