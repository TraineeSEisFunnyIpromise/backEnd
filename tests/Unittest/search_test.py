import unittest
from unittest.mock import patch, AsyncMock
import asyncio

# Import your functions

from reqandscrape.NDcalculate import normal_dist
from reqandscrape.search_scrape.PWBDscraperAZ import item_sorting,get_asin,urlcleaner,clean_html,get_reviews,get_product_detail

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
        result = get_asin()
        self.assertIsNotNone(result)
    
    def test_clean_html(self):
        html = "<html><head><title>Test</title></head><body><h1>Test</h1><p>Test</p></body></html>"
        result = clean_html(html)
        self.assertIsNotNone(result)

    @patch('Reqandscrape.Search_scrape.PWBDscraperAZ.requests.get')
    def test_get_reviews(self, mock_get):
        mock_response = AsyncMock()
        mock_response.text = '<div class="review-container"><a class="review-title">Great product</a><span class="review-text">I love it</span><i class="review-rating">5 stars</i></div>'
        mock_get.return_value = mock_response

        response = mock_get('https://www.amazon.com/dp/DP123456')
        result = get_reviews(response)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['review_title'], 'Great product')
        self.assertEqual(result[0]['review_text'], 'I love it')
        self.assertEqual(result[0]['review_rating'], '5 stars')

    @patch('Reqandscrape.Search_scrape.PWBDscraperAZ.requests.get')
    def test_get_product_detail(self, mock_get):
        mock_response = AsyncMock()
        mock_response.text = '<div id="feature-bullets"><li>Feature 1</li><li>Feature 2</li></div><i data-hook="average-star-rating">4.5 out of 5 stars</i><div data-hook="total-review-count">100 reviews</div>'
        mock_get.return_value = mock_response

        response = mock_get('https://www.amazon.com/dp/DP123456')
        result = get_product_detail(response)
        self.assertIsNotNone(result)
        self.assertEqual(result[0]['stars'], '4.5 out of 5 stars')
        self.assertEqual(result[0]['rating_count'], '100 reviews')
        self.assertEqual(result[0]['feature_bullets'], ['Feature 1', 'Feature 2'])

        


if __name__ == '__main__':
    unittest.main()
                        
