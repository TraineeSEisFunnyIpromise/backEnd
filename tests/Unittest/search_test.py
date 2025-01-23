import unittest

import asyncio
from bs4 import BeautifulSoup  # For HTML parsing (if needed)
# Import your functions

from Reqandscrape.NDcalculate import normal_dist
from Reqandscrape.search_scrape.PWBDscraperAZ import item_sorting,get_asin,urlcleaner,clean_html,get_reviews,get_product_detail

class TestSearchReview(unittest.TestCase):


    def test_urlcleaner(self):
        url = ["https://urlaodbgouabmedialsndlf./dp520951/askfn.com","https://urlaodbgouabmedialsndlf./dp78902/askfn.com","https://urlaodbgouabmedialsndlf./askfn.com","https://amazon.mediasfkagli.lhjepa./dp684951/askfn.com"]
        result = urlcleaner(url)
        self.assertIsNone(result)

    def test_item_sorting(self):
        items = parse_txt_to_bs4("success_raw_result.txt")
        result = item_sorting(items)
        print(result)
        self.assertIsNotNone(result)

    def test_get_asin(self):
        result = get_asin()
        self.assertIsNotNone(result)
    
    def test_clean_html(self):
        html = "<html><head><title>Test</title></head><body><h1>Test</h1><p>Test</p></body></html>"
        result = clean_html(html)
        self.assertIsNotNone(result)


    def test_get_reviews(self, mock_get):

        response = parse_txt_to_bs4("success_raw_result.txt")
        result = get_reviews(response)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertIsNotNone(result[0]['review_title'])
        self.assertIsNotNone(result[0]['review_text'])
        self.assertIsNotNone(result[0]['review_rating'])


    def test_get_product_detail(self, mock_get):

        #'https://www.amazon.com/dp/DP123456'
        response = parse_txt_to_bs4()
        result = get_product_detail(response)
        self.assertIsNotNone(result)
        self.assertIsNotNone(result[0]['stars'])
        self.assertIsNotNone(result[0]['rating_count'])
        self.assertIsNotNone(result[0]['feature_bullets'])

        
def parse_txt_to_bs4(filename):

  try:
    with open(filename, 'r', encoding='utf-8') as file:
      html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup
  except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")
    return None
  except Exception as e:
    print(f"An error occurred: {e}")
    return None


if __name__ == '__main__':
    unittest.main()
                        
