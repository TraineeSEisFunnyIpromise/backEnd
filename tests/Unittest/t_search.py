import unittest
from unittest.mock import patch, AsyncMock
import asyncio

# Import your functions
from Reqandscrape.search_scrape.PWBDscraperAZ import scrape_amazon,get_product_detail,get_reviews,scrape_amazon_product,get_asin,urlcleaner



class TestSearchReview(unittest.TestCase):


    def test_url_cleaner(self):
        url = ["https://urlaodbgouabmedialsndlf./dp520951/askfn.com","https://urlaodbgouabmedialsndlf./dp78902/askfn.com","https://urlaodbgouabmedialsndlf./askfn.com","https://amazon.mediasfkagli.lhjepa./dp684951/askfn.com"]
        max = len(url)
        for i in range(max):
            clean = urlcleaner(url[i])
            print(clean)
    


if __name__ == '__main__':
    unittest.main()
                        
