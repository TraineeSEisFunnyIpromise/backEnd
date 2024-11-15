import unittest
from unittest.mock import patch, AsyncMock
import asyncio

# Import your functions
from Reqandscrape.Search_scrape.PWBDscraperAZ import scrape_amazon,get_product_detail,get_reviews,scrape_amazon_product,get_asin



class TestSearchReview(unittest.TestCase):
    
    asin = ["DP023543","DP546503","DP003156"]
    url = ["","",""]
    soup = open("raw_result_test.txt", "w+",encoding="utf-8")

    def test_success_scrape_review(self,soup):
        result = get_reviews(soup)
        self.assertIsNotNone(result)

    def test_unsuccess_scrape_review(self):
        result = get_reviews([])
        self.assertIsNone(result)

    def test_success_scrape_product_detail(self,soup):
        result = get_product_detail(soup)
        self.assertIsNotNone(result)

    def test_unsuccess_scrape_product_detail(self):
        result = get_product_detail([])
        self.assertIsNone(result)

    def url_cleaner(self):
        print()
    


if __name__ == '__main__':
    unittest.main()
                        
