# importing necessary libraries
import random
import asyncio
import pandas as pd
from datetime import datetime
from playwright.async_api import async_playwright


# Extract the title of a review from a review element
async def extract_review_title(review_element):
    try:
        title = await review_element.evaluate("(element) => element.querySelector('[data-hook=\"review-title\"]').innerText")
        title = title.replace("\n", "")
        title = title.strip()
    except:
        title = "not available"
    return title 


# Extract the body of a review from a review element
async def extract_review_body(review_element):
    try:
        body = await review_element.evaluate("(element) =>  element.querySelector('[data-hook=\"review-body\"]').innerText")
        body = body.replace("\n", "")
        body = body.strip()
    except:
        body = "not available"
    return body

# Extract the colour of the product reviewed from a review element
async def extract_product_colour(review_element):
    try:
        colour = await review_element.evaluate("(element) => element.querySelector('[data-hook=\"format-strip\"]').innerText")
        colour = colour.replace("Colour: ", "")
    except:
        colour = "not available"
    return colour

# Extract the rating of a review from a review element
async def extract_rating(review_element):
    try:
        ratings = await review_element.evaluate("(element) => element.querySelector('[data-hook=\"review-star-rating\"]').innerText")
    except:
        ratings="not available"
    return ratings.split()[0]

# Save the extracted reviews to a csv file
async def save_reviews_to_csv(reviews):
        data = pd.DataFrame(reviews, columns=['product_colour','review_title','review_body','review_date','rating'])
        data.to_csv('amazon_product_reviews15.csv', index=False)

# Perform a request and retries the request if it fails
async def perform_request_with_retry(page, link):
    MAX_RETRIES = 5
    retry_count = 0
    while retry_count < MAX_RETRIES:
        try:
            await page.goto(link)
            break
        except:
            retry_count += 1
            if retry_count == MAX_RETRIES:
                raise Exception("Request timed out")
            await asyncio.sleep(random.uniform(1, 5))

# Extract all reviews from multiple pages of the URL
async def extract_reviews(page):
    reviews =[]
    while True:
        # Wait for the reviews to be loaded
        await page.wait_for_selector("[data-hook='review']")

        # Get the reviews
        review_elements = await page.query_selector_all("[data-hook='review']")
        for review_element in review_elements:
            review_title = await extract_review_title(review_element)
            review_body = await extract_review_body(review_element)
            product_colour = await extract_product_colour(review_element)
            rating = await extract_rating(review_element)
            reviews.append((product_colour,review_title,review_body,rating))

        # Find the next page button
        next_page_button = await page.query_selector("[class='a-last']")
        if not next_page_button:
            break

        # Click the next page button
        await page.click("[class='a-last']")
    return reviews

# Asynchronous Web Scraping of Amazon Product Reviews using Playwright
# Replace with your logic to fetch proxy details (e.g., API call)
import asyncio

async def main():
  proxy_server = f"http://@gate.smartproxy.com:7000"
  async with async_playwright() as p:
    browser = await p.chromium.launch(proxy={  # Global proxy configuration
        "username":"",
        "password":"",
        "server": proxy_server
    }, headless=False)  # Adjust headless mode as needed
    context = await browser.new_context()
    page = await context.new_page()
    target_url="https://www.amazon.com/NQD-Control-Toddlers-Material-Birthday/dp/B0CWQGH32L/ref=sr_1_1_sspa?sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"
    await perform_request_with_retry(page, target_url)
    # Your existing code using the page object
    review = await extract_reviews(page)
    await save_reviews_to_csv(review)

    await page.close()
    await context.close()
    await browser.close()

asyncio.run(main())
