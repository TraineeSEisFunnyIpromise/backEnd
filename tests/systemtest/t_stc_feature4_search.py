import pytest
import asyncio
from playwright.async_api import async_playwright


@pytest.mark.asyncio
async def test_search_success():
  async with async_playwright() as p:
    page = await p.chromium.launch().new_page()

    # Navigate to the application URL
    await page.goto('http://localhost:4000/search')

    # Fill in the search term
    await page.fill('electric fan', 'student')

    # Click the submit button
    await page.click('button[type="submit"]')

    # Wait for results to load (adjust selector if necessary)
    await page.wait_for_selector('.container')

    # Check if search results are displayed
    search_results = await page.query_selector_all('.table tbody tr')
    assert len(search_results) > 0

    # Implement the `highlightText` function as needed

    # Check if price data is displayed (if applicable)
    price_column = await page.query_selector_all('.table thead tr th')[1].inner_text
    assert price_column == 'Price'

    # Check if chart container is visible (assuming logic holds)
    chart_container = await page.query_selector('.chart-container')
    assert await chart_container.is_visible()

    # Close the page
    await page.close()


@pytest.mark.asyncio
async def test_compare_success():
    with async_playwright() as p:
        # Navigate to the application URL
        page = await p.chromium.launch().new_page()

        page.goto('http://localhost:4000/search')

        # Fill in the search term
        page.fill('electric fan', 'student')

        # Click the submit button
        page.click('button[type="submit"]')

        # Wait for results to load (adjust selector if necessary)
        page.wait_for_selector('.container')

        # Check if search results are displayed
        search_results = page.query_selector_all('.table tbody tr')
        assert len(search_results) > 0

        # This requires implementing the `highlightText` function

        # Check if price data is displayed (if applicable)
        price_column = page.query_selector_all('.table thead tr th')[1].inner_text
        assert price_column == 'Price'

        # This test assumes the chart container is displayed only when data is present
        chart_container = page.query_selector('.chart-container')
        assert chart_container.is_visible()
