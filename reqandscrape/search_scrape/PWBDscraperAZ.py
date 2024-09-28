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
URL = "http://www.amazon.com"
api_endpoint = ""


import asyncio
from playwright.async_api import async_playwright
# from Review_scraper.PWRAZscrape import search_review
import random
import regex as re
import csv
import pandas as pd
import json
import bleach
#overhaul entire scraper man this literally similar how to replaced engine
#----------------Selenium scraper------------------------


# Options for Chrome driver
# Navigate to the website
async def scrape_amazon(inputkeyword,seach_group):
	if search_group != "":
		inputkeyword = inputkeyword + " " + search_group
		return inputkeyword
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
  #//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[30]/div/div/span/a[3]
  #//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[28]/div/div/span/a[4]
  #//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[28]/div/div/span/a[5]
  #//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[28]/div/div/span/a[6]
  # 
	while(True):
		try: 
			numberofpages=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH, "//*[@class='s-pagination-item s-pagination-disabled']"))).text
		except TimeoutException: 
			print("The total number of pages was not found.")
			driver.refresh()
			continue
		else:
			break
	print("Total number of pages: ",numberofpages)
	

	content = driver.page_source
	soup = BeautifulSoup(content, 'html.parser')
	items = soup.findAll('div', 'sg-col-inner')

	# #print(type(items))
	# with open("raw_result.txt", "w",encoding="utf-8") as f:
	# 		for item in items:
	# 				text_content = str(item)
	# 				json_data = json.dumps(text_content, indent=4)
	# 				f.write(json_data + "\n")

	
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

	for item_text in items:
			# item_text = BeautifulSoup(item, 'lxml')
			# print(item_text)
			# find name
			#class="a-size-base-plus a-color-base a-text-normal"
			name = item_text.find('span', class_='a-size-medium a-color-base a-text-normal')
			name = clean_html(str(name))
			product_name.append(name)

			price = item_text.find('span', class_='a-price-whole')
			price = clean_html(str(price))
			product_price.append(price)
			
			rating = item_text.find('span', class_='a-row a-size-small')
			rating = clean_html(str(rating))
			product_ratings.append(rating)

			link = item_text.select("[data-asin] h2 a")
			link = clean_html(str(link))
			product_link.append(link)
	save_data_csv(product_name, product_asin, product_price, product_ratings, product_ratings_num, product_link)

#yup get review stuff
def get_reviews(soup):
    review_elements = soup.select("div.review")

    scraped_reviews = []

    for review in review_elements:

        r_rating_element = review.select_one("i.review-rating")
        r_rating = r_rating_element.text.replace("out of 5 stars", "") if r_rating_element else None

        r_title_element = review.select_one("a.review-title")
        r_title_span_element = r_title_element.select_one("span:not([class])") if r_title_element else None
        r_title = r_title_span_element.text if r_title_span_element else None

        r_content_element = review.select_one("span.review-text")
        r_content = r_content_element.text if r_content_element else None

        r_date_element = review.select_one("span.review-date")
        r_date = r_date_element.text if r_date_element else None

        r_verified_element = review.select_one("span.a-size-mini")
        r_verified = r_verified_element.text if r_verified_element else None


        r = {
            "rating": r_rating,
            "title": r_title,
            "content": r_content,
            "date": r_date,
            "verified": r_verified,
        }

        scraped_reviews.append(r)

    return scraped_reviews



def save_data_csv(product_name, product_asin, product_price, product_ratings, product_ratings_num, product_link):

	data = []
	data.append([product_name, product_asin, product_price, product_ratings, product_ratings_num, product_link])
	# Save data to CSV file
	with open('search_result_recent.csv', 'w', newline='',encoding="utf-8") as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(['Product Name', 'ASIN', 'Price', 'Ratings', 'Ratings Num', 'Link'])  # Write header row
			writer.writerows(data)
	# to check data scraped

def save_data_csv_product(product_name, product_asin, product_price, product_ratings):

	data = []
	data.append([product_name, product_asin, product_price, product_ratings])
	# Save data to CSV file
	with open('search_result_product.csv', 'w', newline='',encoding="utf-8") as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(['Title', 'ASIN', 'Price', 'Product_Ratings', 'Ratings Score', 'Link'])  # Write header row
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

async def scrape_amazon_product(asin):
	URL_link = asin
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
	driver.get("https://www.amazon.com/dp/"+URL_link)

	# Log network requests after navigation
	for request in driver.requests:
			print(f"Request: {request.method} {request.url}")  # Inspect requests

	driver.implicitly_wait(4)


	driver.implicitly_wait(5) 

	#class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"
  #//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[30]/div/div/span/a[3]
  #//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[28]/div/div/span/a[4]
  #//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[28]/div/div/span/a[5]
  #//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[28]/div/div/span/a[6]
  #
	content = driver.page_source
	soup = BeautifulSoup(content, 'html.parser')
	items = soup.findAll('div', 'sg-col-inner')

	#print(type(items))
	with open("raw_result_product.txt", "w",encoding="utf-8") as f:
			for item in items:
					text_content = str(item)
					json_data = json.dumps(text_content, indent=4)
					f.write(json_data + "\n")
	#set data from search
	#review scraping begin
	#print("Item : ",items)
	
	# end process quit driver
	driver.quit()
    
def json_data_mock():
	input_file= "Reqandscrape\sample.json"
	with open(input_file, encoding="utf-8") as json_file:
		parsed_json = json.load(json_file)
	return parsed_json

def clean_html(input):
    # Reaplce html tags from user input, see utils.test for examples

    ok_tags = [u"a", u"img", u"strong", u"b", u"em", u"i", u"u", u"ul", u"li", u"p", u"br",  u"blockquote", u"code",u"\n"]
    ok_attributes = {u"a": [u"href", u"rel"], u"img": [u"src", u"alt", u"title"]}
    # all other tags: replace with the content of the tag

    # If input contains link in the format:  then convert it to &lt; http:// &gt;
    # This is because otherwise the library recognizes it as a tag and breaks the link.
    input = re.sub("\&lt;(http\S+?)\&gt;", r'&lt; \1 &gt;', input)

    cleaner = bleach.Cleaner(
            # attributes=ok_attributes,
            # tags=ok_tags,
            strip=True)
    output = cleaner.clean(input)
    return output


def test():
	input_file = open("raw_result.txt","r",encoding="utf-8")
	input_file_convert = BeautifulSoup(str(input_file),"lxml")
	for items in input_file_convert:
		result = item_sorting(items)
		print(result)

# when want to use it independently
# search_term = input("Please type some input: ")
# # from reqandscrape.requestsender.chatgptreqsender import receiveinput
search_term = "binocular"
search_group = ""
asyncio.run(scrape_amazon(search_term,search_group))
