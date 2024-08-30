import asyncio
from playwright.async_api import async_playwright
# from Review_scraper.PWRAZscrape import search_review
# from URLcleaner import urlcleaner
import regex as re
import csv
import pandas as pd
import json
#inport file for cors
from flask import Flask
from flask_cors import CORS
# instantiate the app
app = Flask(__name__)
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
#----------------------finding prod--------------------------------
URL = "https://www.amazon.com"
bright_data_key = ""

async def scrape_amazon(search_term, search_group):
    async with async_playwright() as p:
        if (search_group != '' and search_group != None):
            search = search_term + " for " + search_group

        browser = await p.chromium.connect_over_cdp(bright_data_key)
        page = await browser.new_page()
        # target_URL = URL + re.sub(r"\s+", "+", search)
        await page.goto(URL)
        print("======finding search=====")
        # Enter search term and get product data
        #twotabsearchtextbox
        #nav-search-submit-button
        await page.fill("#twotabsearchtextbox", search)
        await page.press("#nav-search-submit-button", "Enter")
        print("=======doing parse=========")
        #.s-main-slot.s-result-list.s-search-results.sg-row
        await page.wait_for_selector(".s-widget-container")
        products = await parse_results(page)
        print("======Done parse=====")
        # For each product, scrape reviews and add them to the product data
        
        for idx, product in enumerate(products):
            asin = urlcleaner(product["url"])  # Function to extract ASIN from URL
            reviews = await search_review(asin)  # Scrape reviews using your review scraping function
            product["reviews"] = reviews  # Add reviews to the product data
            product["id"] = idx + 1  # Add a unique id to each product
        print("======Done review=====")
        # Save the combined data
        await save_data(products)
        print("======closing headless browser=====")
        await browser.close()
        print("======sending result=====")
        return products

#-------------------after this line it all about the function that use above-------

#note this should create a seperate file but for some reason it can't find the file that contain
#the fuction but this function consume too much time than it should soo.....brute force style

async def parse_results(page):
    return await page.evaluate('''() => {
        return Array.from(document.querySelectorAll(".s-widget-container")).map(el => {
            return {
                url: el.querySelector("a")?.getAttribute("href"),
                title: el.querySelector("h2 span")?.innerText,
                price: el.querySelector(".a-price > .a-offscreen")?.innerText,
                rating: el.querySelector(".a-icon-alt")?.innerText,
            };
        });
    }''')

async def save_data(data):
        filename = pd.read_csv('_temporary_save.csv')
        print("Jsoning data")
        data_json = json.dumps(data)
        # Clean data (example: remove duplicates, handle missing values)
        filename.drop_duplicates()
        filename.fillna(0, inplace=True)

        print('Response Scraped Body: ', data_json)
        with open(filename, "w") as outfile:
            outfile.write(data_json)

#--------------------------URL cleaner---------------------------------------

def is_asin(text):
    # ASINs are typically 10-character alphanumeric strings..nice
    return bool(re.fullmatch(r'[A-Z0-9]{10}', text, flags=re.IGNORECASE))

def urlcleaner(input_file):
    result = []
    json_object = json.load(input_file)
    filtered_lines = [line for line in json_object if line.get("url")]

    for line in filtered_lines:
        url = line.get("url")
        #culling the URL
        asin_match = re.search(r'/[dg]p/([^/?]+)', url, flags=re.IGNORECASE)
        if asin_match:
            asin = asin_match.group(1)
            # check is it a valid ASIN
            if is_asin(asin):
                result.append(asin)
    return result
#----------------review scraping---------------------

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

async def extract_description_body(review_element):
    try:#featurebullets_feature_div
        body = await review_element.evaluate("(element) => element.querySelector('[data-hook=\"featurebullets_feature_div\"]').innerText")
        body = body.replace("\n", "").strip()
    except:
        body = "not available"
    return body

# #productDetails_feature_div
async def extract_description_body_extra(review_element):
    try:#featurebullets_feature_div
        body = await review_element.evaluate("(element) => element.querySelector('[data-hook=\"productDetails_feature_div\"]').innerText")
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

async def save_reviews_to_csv(reviews, filename='_amazon_product_reviews.csv'):
    data = pd.DataFrame(reviews, columns=['review_title', 'review_body', 'rating'])
    data.to_csv(filename, mode='a', header=False, index=False)

async def perform_request_with_retry(page, link):
    MAX_RETRIES = 5
    retry_count = 0

    while retry_count < MAX_RETRIES:
        try:
            # Use the proxy URL
            await page.goto(link)
            break
        except Exception as e:
            retry_count += 1
            print(f"Request failed: {e}, retrying {retry_count}/{MAX_RETRIES}")
            if retry_count == MAX_RETRIES:
                raise Exception("Request timed out after multiple retries")
            await asyncio.sleep(random.uniform(1, 5))

# #---------extract review like scraped it-------------------
async def extract_reviews(page):
    reviews = []
    while True:
        # await page.wait_for_selector("[data-hook='featurebullets_feature_div']")
        # review_elements = await page.query_selector_all("[data-hook='feature-bullets']")
        # for review_element in review_elements:
        #     desctiption_body = extract_description_body()
        await page.wait_for_selector("[data-hook='review']")
        description_elements = await page.query_selector_all("[data-hook='review']")
        for description_element in description_elements:
            rating  = await extract_rating(review_element)
            reviews.append((review_title, review_body, rating))

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

#--------------the function that use all review task and combine to one-------------------
async def search_review(asin):
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(bright_data_key)
        context = await browser.new_context()
        page = await context.new_page()

        target_url = f"https://www.amazon.com/dp/{asin}"
        await perform_request_with_retry(page, target_url)
        reviews = await extract_reviews(page)

        await page.close()
        await context.close()
        await browser.close()
        return reviews


def search_review_test(inputa,inputb):
    result = "sameple text"
    return result

#----test----
def noasync_amazonscrape(inputa,inputb):
    result = scrape_amazon(inputa,inputb)
    return result
    
def json_data_mock():
	input_file= "Reqandscrape\sample.json"
	with open(input_file, encoding="utf-8") as json_file:
		parsed_json = json.load(json_file)
	return parsed_json

# when want to use it independently
# search_term = input("Please type some input: ")
# from reqandscrape.requestsender.chatgptreqsender import receiveinput