import playwright.sync_api as pw

def test_search(page):
    # Navigate to the application URL
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

with pw.chromium() as browser:
    page = browser.new_page()
    test_search(page)
    page.close()