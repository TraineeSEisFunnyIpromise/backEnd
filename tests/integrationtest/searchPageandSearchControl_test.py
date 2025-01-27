import unittest
from unittest.mock import patch, MagicMock, mock_open
from Reqandscrape.search_scrape.PWBDscraperAZ import (
    scrape_amazon,
    item_sorting,
    get_asin,
    urlcleaner,
    scrape_amazon_product,
    get_reviews,
    get_product_detail,
    clean_html
)
import json

class TestScraper(unittest.TestCase):
    @patch("PWBDscraperAZ.webdriver.Remote")
    @patch("PWBDscraperAZ.WebDriverWait")
    @patch("PWBDscraperAZ.BeautifulSoup")
    def test_scrape_amazon(self, mock_soup, mock_wait, mock_driver):
        mock_driver_instance = MagicMock()
        mock_driver.return_value = mock_driver_instance
        mock_soup_instance = MagicMock()
        mock_soup.return_value = mock_soup_instance
        
        # Simulate a successful scrape
        mock_driver_instance.find_element.return_value = MagicMock()
        mock_soup_instance.find_all.return_value = ["<div>Mock Item</div>"]
        
        result = scrape_amazon("test keyword", "test group")
        self.assertIsNotNone(result)

    @patch("builtins.open", new_callable=mock_open, read_data='[{"asin": "B000123"}]')
    @patch("json.load")
    def test_item_sorting(self, mock_json_load, mock_open_file):
        mock_json_load.return_value = [{"asin": "B000123"}]
        mock_items = [MagicMock()]
        mock_items[0].find.side_effect = [MagicMock(text="Product Name"), None, None, None]
        
        item_sorting(mock_items)
        mock_open_file.assert_called_once_with('temporary_search_result.json', 'w', encoding='utf-8')

    @patch("builtins.open", new_callable=mock_open, read_data='[{"asin": "B000123"}]')
    @patch("json.load")
    def test_get_asin(self, mock_json_load, mock_open_file):
        mock_json_load.return_value = [{"asin": "B000123"}]
        asin_list = get_asin()
        self.assertEqual(asin_list, ["B000123"])

    def test_urlcleaner(self):
        url = "https://www.amazon.com/dp/B000123"
        cleaned_url = urlcleaner(url)
        self.assertEqual(cleaned_url, "B000123")

    @patch("PWBDscraperAZ.requests.get")
    @patch("PWBDscraperAZ.get_product_detail")
    @patch("PWBDscraperAZ.get_reviews")
    @patch("builtins.open", new_callable=mock_open, read_data='[{"asin": "B000123"}]')
    def test_scrape_amazon_product(self, mock_open_file, mock_get_reviews, mock_get_product_detail, mock_requests):
        mock_requests.return_value.status_code = 200
        mock_requests.return_value.text = "Mock HTML"
        mock_get_product_detail.return_value = [{"description": "Test description"}]
        mock_get_reviews.return_value = {"Review Titles": ["Test Title"], "Review Texts": ["Test Review"]}

        scrape_amazon_product(["B000123"])
        mock_open_file.assert_called_with('temporary_search_result.json', 'r+')

    @patch("PWBDscraperAZ.BeautifulSoup")
    def test_get_reviews(self, mock_soup):
        mock_soup_instance = MagicMock()
        mock_soup.return_value = mock_soup_instance
        mock_soup_instance.find_all.side_effect = [["Mock Title"], ["Mock Review"], ["Mock Rating"]]

        reviews = get_reviews(MagicMock(status_code=200, text="Mock HTML"))
        self.assertIn("Review Titles", reviews)
        self.assertIn("Review Texts", reviews)

    def test_get_detail(self, mock_soup):
        mock_soup_instance = MagicMock()
        mock_soup.return_value = mock_soup_instance
        mock_soup_instance.find_all.side_effect = [["Mock Title"], ["Mock Review"], ["Mock Rating"]]

        reviews = get_product_detail(MagicMock(status_code=200, text="Mock HTML"))
        self.assertIn("Review Titles", reviews)
        self.assertIn("Review Texts", reviews)

    def test_clean_html(self):
        raw_html = "<p>This is a <b>test</b>.</p>"
        cleaned = clean_html(raw_html)
        self.assertEqual(cleaned, "This is a test")

if __name__ == "__main__":
    unittest.main()