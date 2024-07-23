import unittest
from unittest.mock import patch, AsyncMock
import asyncio

# Import your functions
from reqandscrape.search_scrape.PWBDscraperAZ import run, parse_results

class TestProductSearch(unittest.TestCase):

  async def test_run_with_search_term(self):
          with patch('builtins.input', return_value='electronics'):
            asyncio.run(run())
          with patch('playwright.async_api.async_playwright.chromium.connect_over_cdp') as mock_connect:
            mock_connect.return_value = AsyncMock()
            with patch('playwright.page.Page.goto') as mock_goto:
                mock_goto.return_value = None
                with patch('playwright.page.Page.wait_for_selector') as mock_wait:
                    mock_wait.return_value = None

                    async def parse_results(page):
                        return [
                            {"url": "https://www.amazon.com/product1", "title": "Product 1", "price": "$10.99"},
                            {"url": "https://www.amazon.com/product2", "title": "Product 2", "price": "$25.50"},
                        ]
                    with patch('your_file.parse_results', parse_results):
                        await run()


