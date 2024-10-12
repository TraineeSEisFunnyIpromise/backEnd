

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

def clear_csv(csv_file):
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([])
# Navigate to the website

def scrape_amazon(inputkeyword,search_group):
	time = 0
	print("\t start amazon")
	result = []

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
	print("start process")
	if(api_endpoint != ''):
		try:
			print("\t\t processing")
			# Replace with your proxy server URL
			options.add_argument(f'--proxy-server={api_endpoint}')
			# Create a Selenium Wire driver
			driver = webdriver_wire.Chrome(options=options,seleniumwire_options=seleniumwire_options_setting)
			driver.get("https://www.amazon.com")

			driver.implicitly_wait(5)
			#merge word
			inputkeyword = inputkeyword + " " + search_group
			keyword = str(inputkeyword)
			#finding search box
			search = driver.find_element(By.ID, 'twotabsearchtextbox')
			#set condition if detected abandon task
			search.send_keys(keyword)
				# click search button
			driver.implicitly_wait(2)
			search_button = driver.find_element(By.ID, 'nav-search-submit-button')
				
			search_button.click()
			wait_count = 0
			driver.implicitly_wait(8) 
			print("before looping")
			while True:
				print("looping")
				driver.implicitly_wait(8)
				try:
								#class="s-pagination-item s-pagination-button"
								driver.implicitly_wait(8)
								next_button = driver.find_element(By.XPATH, "//a[text()='Next']")
								next_button.click()
								wait_count = 0
				except (NoSuchElementException, TimeoutException):
					wait_count += 1
					if wait_count >= 50 // 2:  # Check after half of max wait time
						print("Error: Encountered delays for too long")
						break  # Exit the loop if exceeded maximum wait attempts
			print("end of loop")

			content = driver.page_source
			soup = BeautifulSoup(content, 'html.parser')
			items = soup.findAll('div', 'sg-col-inner')
			print("setting up data")
			#print(type(items))
			with open("raw_result.txt", "w+",encoding="utf-8") as f:
					print("enter loop raw result")
					for item in items:
							text_content = str(item)
							json_data = json.dumps(text_content, indent=4)
							f.write(json_data + "\n")
			print("item sorting")
			item_sorting(items)
				#setting up ASIN
			print("setting up asin")
			asin_set = get_asin()
			#begin product scraping
			print("check asin for product scraping")
			if asin_set is list and asin_set is not None:
				print("scraping")
				# scrape_amazon_product(asin_set)
			else:
				print("Product scraping failed")
				# end process quit driver
			print("end of product scraping")
			driver.quit()
			print("\t\t end process")
		except(ConnectionRefusedError,ConnectionAbortedError):
			driver.quit()
			print("\t\t end process")
	else:
		print("no proxy")
		driver.quit()

	with open('search_result3.json', 'w', encoding='utf-8') as json_file:
		json.dump(result, json_file, ensure_ascii=False, indent=4)
	print("\t end amazon")
	if result == None:
		print("result bad")
		result = "bad"
	
	return result

def item_sorting(items):
			data = []
			data_name = []
			data_price = []
			data_ratings = []
			data_link = []
			data_asin = []

				# Clear the CSV file	
			with open('search_result2.json', 'w', encoding='utf-8') as jsonfile:
					json.dump([], jsonfile)
			with open('search_result3.json', 'w', encoding='utf-8') as jsonfile:
					json.dump([], jsonfile)

			for item_text in items:
					product_name = clean_html(str(item_text.find('span', class_='a-size-medium a-color-base a-text-normal')))
					data_name.append(product_name)
					product_price = clean_html(str(item_text.find('span', class_='a-price-whole')))
					data_price.append(product_price)
					product_ratings = clean_html(str(item_text.find('span', class_ = 'a-size-base a-color-base')))
					data_ratings.append(product_ratings)
					product_link = str(item_text.find('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'))
					product_link = urlcleaner(product_link)
					data_link.append(product_link)
					product_asin = urlcleaner(product_link)
					data_asin.append(urlcleaner(product_link))

					# Calculate product_asin using urlcleaner (if needed)
					# product_asin = urlcleaner(product_link)
					
					# Create a dictionary for each product
					if product_name != None:
						product_data = {
								"product": product_name,
								"price": product_price,
								"rating": product_ratings,
								"URL": product_link,
								"ASIN": product_asin
						}
						data.append(product_data)
						# if(product_data['product'] is not None):
						#     data.append(product_data)
			# Write data to JSON
			with open('search_result3.json', 'a', encoding='utf-8') as jsonfile:
					if jsonfile['product_name']:
						print("bad")
					else:	
					  json.dump(data, jsonfile, indent=4)
			

def get_asin():
	data=[]
	with open('search_result3.json', 'a', encoding='utf-8') as jsonfile:
				if jsonfile['ASIN']== None:
					print("bad")
				else:	
					json.dump(data, jsonfile, indent=4)
	return data


# #--------------------------URL cleaner---------------------------------------

def is_asin(text):
    # ASINs are typically 10-character alphanumeric strings..nice
    return bool(re.fullmatch(r'[A-Z0-9]{10}', text, flags=re.IGNORECASE))

def urlcleaner(url):
    result = ''
        #culling the URL
    asin_match = re.search(r'/[dg]p/([^/?]+)', url, flags=re.IGNORECASE)
    if asin_match:
            asin = asin_match.group(1)
            # # check is it a valid ASIN
            if is_asin(asin):
                result = asin
    return result
# #----------------review scraping---------------------

def scrape_amazon_product(asin):
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


	for i in asin:
		driver.get("https://www.amazon.com/dp/" + asin[i])
		content = driver.page_source
		soup = BeautifulSoup(content, 'html.parser')
		items = soup.findAll('div', 'sg-col-inner')
		get_product_detail(soup)
		get_reviews(soup)
		with open("raw_result_product.txt", "w",encoding="utf-8") as f:
			for item in items:
					text_content = str(item)
					json_data = json.dumps(text_content, indent=4)
					f.write(json_data + "\n")
		
	# Log network requests after navigation
	for request in driver.requests:
			print(f"Request: {request.method} {request.url}")  # Inspect requests

	driver.implicitly_wait(4)
	# end process quit driver
	driver.quit()

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

def get_product_detail(soup):
	product_cards = soup.find_all('div', {'data-component-type': 's-search-result'})

	for card in product_cards:
		# Product Name
		product_name = card.find('span', {'class': 'a-size-medium a-color-base a-text-normal'})
		if product_name:
			product_name = product_name.text.strip()
		else:
			product_name = 'Not available'

		# Price
		price = card.find('span', {'class': 'a-price-whole'})
		if price:
			price = price.text.strip()
		else:
			price = 'Not available'

		# Rating
		rating = card.find('span', {'class': 'a-icon-alt'})
		if rating:
			rating = rating.text.split()[0]
		else:
			rating = 'Not available'

		# Number of Ratings
		num_ratings = card.find('span', {'class': 'a-size-base'})
		if num_ratings:
			num_ratings = num_ratings.text.split()[0]
			if num_ratings == "M.R.P:":
				num_ratings = 'Not available'
		else:
			num_ratings = 'Not available'

		# Past Month Bought
		past_month_bought = card.find('span', {'class': 'a-size-base a-color-secondary'})
		if past_month_bought:
			past_month_bought = past_month_bought.text.strip()
			if past_month_bought == "M.R.P:":
				past_month_bought = 'Not available'
		else:
			past_month_bought = 'Not available'

	

def json_data_mock():
	input_file= "search_result3.json"
	with open(input_file, encoding="utf-8") as json_file:
		parsed_json = json.load(json_file)
	return parsed_json

def csv_json_mock():
	with open('search_result3.json', 'w', encoding='utf-8') as json_file:
		json.dump(result, json_file, ensure_ascii=False, indent=4)
	print("\t end amazon")
	if result == None:
		print("result bad")
		result = "bad"
	
	return result
	# with open(input_file, encoding="utf-8") as json_file:
	# 	print(json_file)
	# 	parsed_json = json.load(json_file)
	# jsoned_file = json.dumps(parsed_json,indent=4)
	# return jsoned_file
	

def clean_html(input):
    cleaner = bleach.Cleaner(
            strip=True
						)
    output = cleaner.clean(input)
    return output