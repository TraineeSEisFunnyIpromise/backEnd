import unittest
from unittest.mock import patch, AsyncMock
import asyncio

# Import your functions

from Reqandscrape.NDcalculate import normal_dist
from Reqandscrape.Search_scrape.PWBDscraperAZ import item_sorting,get_asin,urlcleaner,clean_html

class TestSearchReview(unittest.TestCase):


    def test_urlcleaner(self):
        url = ["https://urlaodbgouabmedialsndlf./dp520951/askfn.com","https://urlaodbgouabmedialsndlf./dp78902/askfn.com","https://urlaodbgouabmedialsndlf./askfn.com","https://amazon.mediasfkagli.lhjepa./dp684951/askfn.com"]
        result = urlcleaner(url)
        self.assertIsNone(result)

    def test_item_sorting(self):
        items = [{'price': 10},{'price': 5},{'price': 20},{'price': 15}]
        result = item_sorting(items)
        self.assertIsNotNone(result)

    def test_get_asin(self):
        items = [{'asin': 'DP123456'},{'asin': 'DP456789'},{'asin': 'DP789012'}]
        result = get_asin(items)
        self.assertIsNotNone(result)
    
    def test_clean_html(self):
        html = "<html><head><title>Test</title></head><body><h1>Test</h1><p>Test</p></body></html>"
        result = clean_html(html)
        self.assertIsNotNone(result)
        
        


if __name__ == '__main__':
    unittest.main()
                        
