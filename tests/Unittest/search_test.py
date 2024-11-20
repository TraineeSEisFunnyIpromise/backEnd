import unittest
from unittest.mock import patch, AsyncMock
import asyncio

# Import your functions
from Reqandscrape.search_scrape.PWBDscraperAZ import urlcleaner



class TestSearchReview(unittest.TestCase):


    def test_url_cleaner(self):
        url = ["https://urlaodbgouabmedialsndlf./dp520951/askfn.com","https://urlaodbgouabmedialsndlf./dp78902/askfn.com","https://urlaodbgouabmedialsndlf./askfn.com","https://amazon.mediasfkagli.lhjepa./dp684951/askfn.com"]
        max = len(url)
        for i in range(max):
            clean = urlcleaner(url[i])
            print(clean)
    


if __name__ == '__main__':
    unittest.main()
                        
