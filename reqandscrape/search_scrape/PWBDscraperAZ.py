

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
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By


#inport file for cors
from flask import Flask
from flask_cors import CORS
# instantiate the app

# enable CORS

#----------------------finding prod--------------------------------

api_endpoint = ""
AUTH = ''
SBR_WEBDRIVER = f'https://{AUTH}@'

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

	#selenium option 
	sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
	#end of seleniumwire option
	print("start process")
	if(api_endpoint != ''):
		try:
				print("\t\t processing")
				# Replace with your proxy server URL
				# options.add_argument(f'--proxy-server={api_endpoint}')
				# Create a Selenium Wire driver
				inputkeyword = inputkeyword + " " + search_group
				keyword = str(inputkeyword)
				
    	 
				driver = Remote(sbr_connection, options=options) 
				
				driver.get("https://amazon.com")

				#wait for 5 second
				driver.implicitly_wait(500)
				#<input autocomplete="off" spellcheck="false" placeholder="Type characters" 
				# id="captchacharacters" name="field-keywords" class="a-span12" 
				# autocapitalize="off" autocorrect="off" type="text">

				#merge word
				
				#finding search box
				driver.set_page_load_timeout(30)
				search = driver.find_element(By.ID, 'twotabsearchtextbox')
				#set condition if detected abandon task
				search.send_keys(keyword)
					# click search button
				driver.implicitly_wait(2)
				search_button = driver.find_element(By.ID, 'nav-search-submit-button')

				# if(driver.find_element(By.ID,'captchacharacters') == True):
				# 	driver.quit()
				# 	return "detected capcha abandon task"
				
				search_button.click()
				wait_count = 0
				page_limit = 0
				driver.implicitly_wait(800) 
				print("before looping")
				while True and page_limit <= 5:
					print("looping")
					driver.implicitly_wait(500)
					try:
									#class="s-pagination-item s-pagination-button"
									driver.implicitly_wait(400)
									next_button = driver.find_element(By.XPATH, "//a[text()='Next']")
									next_button.click()
									wait_count = 0
									page_limit += 1
					except Exception:
						wait_count += 1
						if wait_count >= 20 // 2:  # Check after half of max wait time
							print(wait_count)
							print("Error: Encountered delays for too long")
							driver.quit()
							break  # Exit the loop if exceeded maximum wait attempts
				print("end of loop")

				content = driver.page_source
				soup = BeautifulSoup(content, 'html.parser').decode("utf-8")
				items = soup.findAll('div', class_='sg-col-inner')
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

				print("quit old driver")
				driver.quit()

				asin_set = get_asin()
				# begin product scraping
				print("check asin for product scraping")
				if isinstance(asin_set, list) and asin_set:
						print("scraping")
						print("setting up new driver")
						for asin in asin_set:
								print("scraping product")
								try:
									scrape_amazon_product(asin)
								except Exception as e:
									print(f"An error occurred while scraping product {asin}: {e}")
						# scrape_amazon_product(asin_set)
				else:
						print("Product scraping failed")
						print("Product search is scraped but detail is ignored")
					# end process quit driver
				print("end of product scraping")
				print("\t\t end process")
		except Exception as e:
				print(f"An error occurred: {e}")
				print("\t\t end process")
				return None
		finally:
				driver.quit()
	else:
		print("no proxy")
		driver.quit()
	
	print("\t end amazon")
#
	print("\t count and add the ID")
	with open('temporary_search_result.json', 'r', encoding='utf-8') as json_file:
		data = json.load(json_file)
	id_count = 1
	for item in data:
		if 'id' not in item:
			item['id'] = id_count
			id_count += 1
		json.dump(data, json_file, ensure_ascii=False, indent=4)
	# for i, item in enumerate(data, start=1):
	# 	item['id'] = i
		print("\t finalized data")
	with open('temporary_search_result.json', 'r', encoding='utf-8') as json_file:
		json.dump(result, json_file, ensure_ascii=False, indent=4)

	print("\t sending")
	if result == None:
		print("result bad")
		result = "bad"
		print("\t end amazon")
	print("\t Success")
	return result

def item_sorting(items):
			data = []
			data_name = []
			data_price = []
			data_ratings = []
			data_link = []
			data_asin = []

			with open('temporary_search_result.json', 'w', encoding='utf-8') as jsonfile:
					json.dump([], jsonfile)

			for item_text in items:
					product_name = str(item_text.find('span', class_='a-size-medium a-color-base a-text-normal'))
					data_name.append(product_name)
					product_price = str(item_text.find('span', class_='a-price-whole'))
					data_price.append(product_price)
					product_ratings = str(item_text.find('span', class_ = 'a-size-base a-color-base'))
					data_ratings.append(product_ratings)
					product_link = str(item_text.find('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'))
					data_link.append(product_link)
					product_asin = urlcleaner(product_link)
					data_asin.append(urlcleaner(product_link))

					# Calculate product_asin using urlcleaner (if needed)
					# product_asin = urlcleaner(product_link)
					# product_name = clean_html(str(item_text.find('span', class_='a-size-medium a-color-base a-text-normal')))
					# data_name.append(product_name)
					# product_price = clean_html(str(item_text.find('span', class_='a-price-whole')))
					# data_price.append(product_price)
					# product_ratings = clean_html(str(item_text.find('span', class_ = 'a-size-base a-color-base')))
					# data_ratings.append(product_ratings)
					# product_link = clean_html(str(item_text.find('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')))
					# data_link.append(product_link)
					# product_asin = urlcleaner(product_link)
					# data_asin.append(urlcleaner(product_link))
					# Create a dictionary for each product
					if product_name:
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
			with open('temporary_search_result.json', 'w', encoding='utf-8') as jsonfile:
				json.dump(data, jsonfile, indent=4)
			

def get_asin():
    data = []
    with open('temporary_search_result.json', 'r+') as jsonfile:
        if jsonfile:
            json_data = json.load(jsonfile)
            for asin in json_data:
                if asin['asin']!=None:
                    data.append(asin)
                else:
                    print("Empty ASIN found.")
    print("asin data")
    print(data)
    return data


# #--------------------------URL cleaner---------------------------------------

def urlcleaner(url):
    clean_url = ''
        #culling the URL
    asin_match = re.search(r'/[dg]p/([^/?]+)', url, flags=re.IGNORECASE)
    if asin_match:
            asin = asin_match.group(1)
            # # check is it a valid ASIN
            clean_url = re.fullmatch(r'[A-Z0-9]{10}', asin, flags=re.IGNORECASE)
    return clean_url
# #----------------review scraping---------------------

def scrape_amazon_product(asin,json_file = open('temporary_search_result.json','w',encoding='utf-8')):
	options = webdriver.ChromeOptions()
	options.add_argument('--incognito')  # Open in incognito mode
	options.add_argument('--disable-extensions')  # Disable extensions
	options.add_argument('--disable-gpu')  # Disable GPU
	options.add_argument('start-maximized')  # Start maximized
	options.add_argument('disable-infobars')  # Disable infobars
	options.add_argument('--blink-settings=imagesEnabled=false')
	# options.add_argument("--headless")
	if(api_endpoint is not None or api_endpoint != ''):
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

			with open("raw_result_product.txt", "w",encoding="utf-8") as f:
				with open(json_file,'r+') as file:
					file_data = json.load(file)
					for item in items:
						text_content = str(item)
						file_data["ASIN"].append(get_product_detail(soup))
						file_data["ASIN"].append(get_reviews(soup))
					json.dump(file_data, file, indent = 4)
			f.write(text_content + "\n")
						
			
		# Log network requests after navigation
		for request in driver.requests:
				print(f"Request: {request.method} {request.url}")  # Inspect requests

		driver.implicitly_wait(4)
		# end process quit driver
		driver.quit()


def get_reviews(soup):
    review_elements = soup.select("div.review")
    print("getting review")
    scraped_reviews = []

    for review in review_elements:
				#review rating
        r_rating_element = review.select_one("i.review-rating")
        r_rating = r_rating_element.text.replace("out of 5 stars", "") if r_rating_element else None
				#review title
        r_title_element = review.select_one("a.review-title")
        r_title_span_element = r_title_element.select_one("span:not([class])") if r_title_element else None
        r_title = r_title_span_element.text if r_title_span_element else None
				#review content
        r_content_element = review.select_one("span.review-text")
        r_content = r_content_element.text if r_content_element else None
				# #review date
        # r_date_element = review.select_one("span.review-date")
        # r_date = r_date_element.text if r_date_element else None


        r = {
            "review_rating": r_rating,
            "title": r_title,
            "content": r_content,
            # "date": r_date,
        }

        scraped_reviews.append(r)

    return scraped_reviews

def get_product_detail(soup):
	product_cards = soup.find_all('div', {'data-component-type': 's-search-result'})
	print("getting detail")
	result = []

	for card in product_cards:

		# description
		description = card.find('span', {'class': ''})
		if description:
			description = description.text.strip()
		else:
			description = 'Not available'

		# Product Rating
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

	r = {
				"product_rating": rating,
				"num_ratings": num_ratings,
				"description": description,
			}
	result.append(r)
    
	return result

def json_data_mock():
	json_file = open('sample.json')
	if json_file == None or json_file == []:
			print("result bad")
	else:
		parsed_json = json.load(json_file)
	return parsed_json

def csv_json_mock():
	result = []
	with open('sample.json', 'r', encoding='utf-8') as json_file:
		if json_file == None:
			print("result bad")
		else:
			result = json.load(json_file)
	print("\t end amazon")
	return result

def clean_html(input):
    cleaner = bleach.Cleaner(
            strip=True
						)
    output = cleaner.clean(input)
    output = str(output)
    return output


def test_prod():
	result = []
	json_file = open('sample.json')
	if json_file == None or json_file == []:
			print("result bad")
	else:
			result = json.load(json_file)
			print(result)
	print("\t end amazon")
	json_file.close()

