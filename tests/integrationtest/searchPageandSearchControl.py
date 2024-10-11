#this test is created in order to test the scraping function which it will test 
import asyncio
from unittest.mock import patch

from Reqandscrape.search_scrape.PWBDscraperAZ import scrape_amazon, clean_html

# Mock data for the search results
MOCK_SEARCH_RESULTS = [
    {
        "product_name": "Test Product 1",
        "price": "$19.99",
        "link": "https://www.amazon.com/product1"
    },
    {
        "product_name": "Test Product 2",
        "price": "$24.95",
        "link": "https://www.amazon.com/product2"
    },
]

# Mock the clean_html function to avoid external dependencies
@patch('your_script.clean_html')

def test_scrape_amazon(mock_clean_html):
    # Set the mock return value for clean_html
    mock_clean_html.return_value = "Cleaned HTML content"

    # Define the search term
    search_term = "test"

    # Run the scraper function in an async loop (if using asyncio)
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(scrape_amazon(search_term, ""))

    # Assert the results (modify based on your expected output)
    assert len(results) == 2  # Expect two products

    for product in results:
        assert product.get("product_name")  # Check for product name
        assert product.get("price")  # Check for price
        assert product.get("link")  # Check for link

def test_scrape_product():
    product_url = ""

def test_scrape_review():
    return

# Run the test
if __name__ == "__main__":
    asyncio.run(test_scrape_amazon())