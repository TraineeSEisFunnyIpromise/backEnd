#import stuff for selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException 
import csv,random,json
from selenium import webdriver
from seleniumwire import webdriver as webdriver_wire
from bs4 import BeautifulSoup

#inport file for cors
from flask import Flask
from flask_cors import CORS
# instantiate the app
app = Flask(__name__)
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
#----------------------finding prod--------------------------------
URL = "https://www.amazon.com"
api_endpoint = ""


import asyncio
from playwright.async_api import async_playwright
# from Review_scraper.PWRAZscrape import search_review
import random
import regex as re
import csv
import pandas as pd
import json
#overhaul entire scraper man this literally similar how to replaced engine
#----------------Selenium scraper------------------------


# Options for Chrome driver
# Navigate to the website
async def scrape_amazon(inputkeyword):
	options = webdriver.ChromeOptions()
	options.add_argument('--incognito')  # Open in incognito mode
	options.add_argument('--disable-extensions')  # Disable extensions
	options.add_argument('--disable-gpu')  # Disable GPU
	options.add_argument('start-maximized')  # Start maximized
	options.add_argument('disable-infobars')  # Disable infobars
	options.add_argument('--blink-settings=imagesEnabled=false')
	# options.add_argument("--headless")

	#seleniumwire option 
	seleniumwire_options_setting = {
    "proxy": {
        "http": api_endpoint,
        "https": api_endpoint
    },
}

	#end of seleniumwire option

	# Replace with your proxy server URL
	options.add_argument(f'--proxy-server={api_endpoint}')
	# Create a Selenium Wire driver
	driver = webdriver_wire.Chrome(options=options,seleniumwire_options=seleniumwire_options_setting)
	driver.get("https://www.amazon.com")

	# Log network requests after navigation
	for request in driver.requests:
			print(f"Request: {request.method} {request.url}")  # Inspect requests

	driver.implicitly_wait(4)

	keyword = str(inputkeyword)
	search = driver.find_element(By.ID, 'twotabsearchtextbox')
	search.send_keys(keyword)

	# click search button
	driver.implicitly_wait(1)
	search_button = driver.find_element(By.ID, 'nav-search-submit-button')
	
	search_button.click()

	driver.implicitly_wait(5) 

	#class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"
	# while True:
  #   # Extract and append data from the current page
  #   extract_and_append(driver, filename)

  #   # Find the "Next" button and click it
  #   next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "next-button")))
  #   next_button.click()

  #   # Increment page number
  #   page_number += 1

  #   # Check if this is the last page (adjust condition as needed)
  #   if page_number > 10:  # Replace 10 with the actual number of pages
  #       break
	while True:
			try:
					#class="s-pagination-item s-pagination-button"
					driver.implicitly_wait(5)
					next_button = driver.find_element(By.CLASS_NAME, "s-pagination-item s-pagination-next s-pagination-button s-pagination-separator")
					next_button.click()
			except (NoSuchElementException, TimeoutException):
					break  # If the "Next" button is not found, assume it's the last page
	content = driver.page_source
	soup = BeautifulSoup(content, 'html.parser')
	items = soup.findAll('div', 'sg-col-inner')

	#print(type(items))
	with open("raw_result.txt", "w",encoding="utf-8") as f:
			for item in items:
					text_content = str(item)
					json_data = json.dumps(text_content, indent=4)
					f.write(json_data + "\n")
	#set data from search
	item_sorting(items)
	#review scraping begin
	#print("Item : ",items)
	
	# end process quit driver
	driver.quit()


def item_sorting(items):
	product_asin = []
	product_name = []
	product_price = []
	product_ratings = []
	product_ratings_num = []
	product_link = []

	for item in items:
			item_text = BeautifulSoup(str(item), 'lxml')
			# print(item_text)
			print("\n")
			print(str(item_text))
			print(type(item_text))
			print("\n\n")
			# find name
			#class="a-size-base-plus a-color-base a-text-normal"
			name = item_text.find('span', class_='a-size-medium a-color-base a-text-normal')
			product_name.append(name)
			price = item_text.find('span', class_='a-price-whole')
			product_price.append(price)
			rating = item_text.find('span', class_='a-row a-size-small')
			product_ratings.append(rating)
			link = item_text.find('span', class_='a-size-medium a-color-base a-text-normal')
			product_link.append(link)
			asin = urlcleaner(link)
			product_asin.append(asin)
	save_data_csv(product_name, product_asin, product_price, product_ratings, product_ratings_num, product_link)


def save_data_csv(product_name, product_asin, product_price, product_ratings, product_ratings_num, product_link):

	data = []
	data.append([product_name, product_asin, product_price, product_ratings, product_ratings_num, product_link])
	# Save data to CSV file
	with open('search_result_recent.csv', 'w', newline='',encoding="utf-8") as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(['Product Name', 'ASIN', 'Price', 'Ratings', 'Ratings Num', 'Link'])  # Write header row
			writer.writerows(data)
	# to check data scraped




# #--------------------------URL cleaner---------------------------------------

def is_asin(text):
    # ASINs are typically 10-character alphanumeric strings..nice
    return bool(re.fullmatch(r'[A-Z0-9]{10}', text, flags=re.IGNORECASE))

def urlcleaner(input_file):
    result = []
    json_object = json.load(input_file)
    for line in json_object:
        url = line.get("url")
        #culling the URL
        asin_match = re.search(r'/[dg]p/([^/?]+)', url, flags=re.IGNORECASE)
        if asin_match:
            asin = asin_match.group(1)
            # check is it a valid ASIN
            if is_asin(asin):
                result.append(asin)
    return result
# #----------------review scraping---------------------

# # import asyncio

# # import pandas as pd
# # from datetime import datetime
# # from playwright.async_api import async_playwright

# async def extract_review_title(review_element):
#     try:
#         title = await review_element.evaluate("(element) => element.querySelector('[data-hook=\"review-title\"]').innerText")
#         title = title.replace("\n", "").strip()
#     except:
#         title = "not available"
#     return title 

# async def extract_review_body(review_element):
#     try:
#         body = await review_element.evaluate("(element) => element.querySelector('[data-hook=\"review-body\"]').innerText")
#         body = body.replace("\n", "").strip()
#     except:
#         body = "not available"
#     return body

# async def extract_description_body(review_element):
#     try:#featurebullets_feature_div
#         body = await review_element.evaluate("(element) => element.querySelector('[data-hook=\"featurebullets_feature_div\"]').innerText")
#         body = body.replace("\n", "").strip()
#     except:
#         body = "not available"
#     return body

# # #productDetails_feature_div
# async def extract_description_body_extra(review_element):
#     try:#featurebullets_feature_div
#         body = await review_element.evaluate("(element) => element.querySelector('[data-hook=\"productDetails_feature_div\"]').innerText")
#         body = body.replace("\n", "").strip()
#     except:
#         body = "not available"
#     return body

# async def extract_rating(review_element):
#     try:
#         ratings = await review_element.evaluate("(element) => element.querySelector('[data-hook=\"review-star-rating\"]').innerText")
#     except:
#         ratings = "not available"
#     return ratings.split()[0]

# async def save_reviews_to_csv(reviews, filename='_amazon_product_reviews.csv'):
#     data = pd.DataFrame(reviews, columns=['review_title', 'review_body', 'rating'])
#     data.to_csv(filename, mode='a', header=False, index=False)

# async def perform_request_with_retry(page, link):
#     MAX_RETRIES = 5
#     retry_count = 0

#     while retry_count < MAX_RETRIES:
#         try:
#             # Use the proxy URL
#             await page.goto(link)
#             break
#         except Exception as e:
#             retry_count += 1
#             print(f"Request failed: {e}, retrying {retry_count}/{MAX_RETRIES}")
#             if retry_count == MAX_RETRIES:
#                 raise Exception("Request timed out after multiple retries")
#             await asyncio.sleep(random.uniform(1, 5))

# # #---------extract review like scraped it-------------------
# async def extract_reviews(page):
#     reviews = []
#     while True:
#         # await page.wait_for_selector("[data-hook='featurebullets_feature_div']")
#         # review_elements = await page.query_selector_all("[data-hook='feature-bullets']")
#         # for review_element in review_elements:
#         #     desctiption_body = extract_description_body()
#         await page.wait_for_selector("[data-hook='review']")
#         review_elements = await page.query_selector_all("[data-hook='review']")
#         for review_element in review_elements:
#             review_title = await extract_review_title(review_element)
#             review_body = await extract_review_body(review_element)
#             rating = await extract_rating(review_element)
#             reviews.append((review_title, review_body, rating))

#         next_page_button = await page.query_selector("[class='a-last']")
#         if not next_page_button or 'disabled' in await next_page_button.get_attribute('class'):
#             break

#         await next_page_button.click()
#     return reviews

# # #--------------the function that use all review task and combine to one-------------------
# async def search_review(asin):
#     async with async_playwright() as p:
#         browser = await p.chromium.connect_over_cdp(bright_data_key)
#         context = await browser.new_context()
#         page = await context.new_page()

#         target_url = f"https://www.amazon.com/dp/{asin}"
#         await perform_request_with_retry(page, target_url)
#         reviews = await extract_reviews(page)

#         await page.close()
#         await context.close()
#         await browser.close()
#         return reviews


# def search_review_test(inputa,inputb):
#     result = "sameple text"
#     return result

# # #----test----
# def noasync_amazonscrape(inputa,inputb):
#     result = scrape_amazon(inputa,inputb)
#     return result
    
def json_data_mock():
	input_file= "Reqandscrape\sample.json"
	with open(input_file, encoding="utf-8") as json_file:
		parsed_json = json.load(json_file)
	return parsed_json

def search_review_test():
	return

# when want to use it independently
# search_term = input("Please type some input: ")
# # from reqandscrape.requestsender.chatgptreqsender import receiveinput
# search_term = "binocular"
# # search_group = ""
# asyncio.run(scrape_amazon(search_term))

def test1():
	items = open("raw_result.txt", "r")
	
	product_asin = []
	product_name = []
	product_price = []
	product_ratings = []
	product_ratings_num = []
	product_link = []

	for item in items:
			item_text = BeautifulSoup(str(item), 'lxml')
			# print(item_text)
			print("\n")
			print(str(item_text))
			print(type(item_text))
			print("\n\n")
			# find name
			#class="a-size-base-plus a-color-base a-text-normal"
			name = item_text.find('span', class_='a-size-medium a-color-base a-text-normal')
			product_name.append(name)
			price = item_text.find('span', class_='a-price-whole')
			product_price.append(price)
			rating = item_text.find('span', class_='a-row a-size-small')
			product_ratings.append(rating)
			link = item_text.find('span', class_='a-size-medium a-color-base a-text-normal')
			product_link.append(link)
			asin = urlcleaner(link)
			product_asin.append(asin)
	save_data_csv(product_name, product_asin, product_price, product_ratings, product_ratings_num, product_link)