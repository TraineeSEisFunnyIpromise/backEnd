import asyncio
import random
import pandas as pd
from datetime import datetime
from playwright.async_api import async_playwright

async def extract_review_title(review_element):
    try:
        title = await review_element.evaluate("(element) => element.querySelector('[data-hook=\"review-title\"]').innerText")
        title = title.replace("\n", "").strip()
    except:
        title = "not available"
    return title 

async def extract_review_body(review_element):
    try:
        body = await review_element.evaluate("(element) => element.querySelector('[data-hook=\"review-body\"]').innerText")
        body = body.replace("\n", "").strip()
    except:
        body = "not available"
    return body

async def extract_rating(review_element):
    try:
        ratings = await review_element.evaluate("(element) => element.querySelector('[data-hook=\"review-star-rating\"]').innerText")
    except:
        ratings = "not available"
    return ratings.split()[0]

async def save_reviews_to_csv(reviews, filename='amazon_product_reviews.csv'):
    data = pd.DataFrame(reviews, columns=['review_title', 'review_body', 'rating'])
    data.to_csv(filename, mode='a', header=False, index=False)

async def perform_request_with_retry(page, link):
    MAX_RETRIES = 5
    retry_count = 0
    while retry_count < MAX_RETRIES:
        try:
            await page.goto(link)
            break
        except Exception as e:
            retry_count += 1
            print(f"Request failed: {e}, retrying {retry_count}/{MAX_RETRIES}")
            if retry_count == MAX_RETRIES:
                raise Exception("Request timed out after multiple retries")
            await asyncio.sleep(random.uniform(1, 5))

async def extract_reviews(page):
    reviews = []
    while True:
        await page.wait_for_selector("[data-hook='review']")
        review_elements = await page.query_selector_all("[data-hook='review']")
        for review_element in review_elements:
            review_title = await extract_review_title(review_element)
            review_body = await extract_review_body(review_element)
            rating = await extract_rating(review_element)
            reviews.append((review_title, review_body, rating))

        next_page_button = await page.query_selector("[class='a-last']")
        if not next_page_button or 'disabled' in await next_page_button.get_attribute('class'):
            break

        await next_page_button.click()
    return reviews

async def search_review(asin):
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("@brd.superproxy.io:9222")
        context = await browser.new_context()
        page = await context.new_page()

        target_url = f"https://www.amazon.com/dp/{asin}"
        await perform_request_with_retry(page, target_url)
        reviews = await extract_reviews(page)
        await save_reviews_to_csv(reviews)

        await page.close()
        await context.close()
        await browser.close()

        return reviews
