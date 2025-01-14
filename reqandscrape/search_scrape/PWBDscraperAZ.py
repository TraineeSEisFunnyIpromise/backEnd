

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
import time
import re
import requests
from parsel import Selector

#inport file for cors
from flask import Flask
from flask_cors import CORS
# instantiate the app

# enable CORS

#----------------------finding prod--------------------------------

username = ''
password = ''
proxy = f"http://{username}:{password}@"
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
#--------------------------Scrape Amazon---------------------------------------

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
	if(proxy != None):
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
				
				with open('temporary_search_result.json', 'w', encoding='utf-8') as jsonfile:
						json.dump([], jsonfile)
				
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
									time.sleep(5)
									next_button = driver.find_element(By.XPATH, "//a[text()='Next']")
									next_button.click()
									wait_count = 0
									page_limit += 1
									content = driver.page_source
									soup = BeautifulSoup(content, 'html.parser')
									items = soup.findAll('div', class_='puisg-row')
									print("item sorting")
									item_sorting(items)
					except Exception:
						wait_count += 1
						if wait_count >= 20 // 2:  # Check after half of max wait time
							print(wait_count)
							print("Error: Encountered delays for too long")
							driver.quit()
							# break  # Exit the loop if exceeded maximum wait attempts
				print("end of loop")


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

		
		finally:
				# driver.quit()
				print("\t end amazon")
			#
				print("\t count and add the ID")
				with open('temporary_search_result.json', 'r', encoding='utf-8') as json_file:
					if(json_file != None or json_file != ''):
						data = json.load(json_file)
						id_count = 1
						for item in data:
							if item is not None:
								if 'id' not in item:
									item['id'] = id_count
									id_count += 1
								json.dump(data, json_file, ensure_ascii=False, indent=4)


					print("\t finalized data")
				with open('temporary_search_result.json', 'w+', encoding='utf-8') as json_file:
					json.dump(result, json_file, ensure_ascii=False, indent=4)

				print("\t sending")
				if result != None:
					print("\t Success")
					return result
				else:
					print("result bad")
					print("\t end amazon")
					return None
	else:
		print("no proxy")
		driver.quit()
		return None
	
	

def item_sorting(items):
			data = []
			data_name = []
			data_price = []
			data_ratings = []
			data_asin = []

			for item_text in items:
					#
					product_name = str(item_text.find('h2',class_="a-size-medium a-spacing-none a-color-base a-text-normal"))
					product_name = clean_html(product_name)
					data_name.append(product_name)
					product_price = str(item_text.find('span', class_='a-price-whole'))
					product_price = clean_html(product_price)
					data_price.append(product_price)
					product_ratings = str(item_text.find('span', class_='a-icon-alt'))
					product_ratings = clean_html(product_ratings)
					data_ratings.append(product_ratings)
					product_link = str(item_text.find("a", class_='a-link-normal s-no-outline'))
					product_asin = urlcleaner(product_link)
					data_asin.append(product_link)
				
					if product_name != None:
						product_data = {
								"product name": product_name,
								"price": product_price,
								"rating": product_ratings,
								"ASIN": product_asin,
								"url":product_link
						}
						data.append(product_data)
						# if(product_data['product'] is not None):
						#     data.append(product_data)
			# Write data to JSON
			with open('temporary_search_result.json', 'w', encoding='utf-8') as jsonfile:
				json.dump(data, jsonfile, indent=4)
			
			return product_data
			

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
		for i in asin:

			url = f'https://www.amazon.com/dp/{i}'

			try:
				response = requests.get(url,proxies = {
				'http': proxy,
				'https': proxy
            })
				
				if response.status_code == 200:
					#open text file
					with open("raw_result_product.txt", "w",encoding="utf-8") as f:
						#open temporary search result.json file
						with open(json_file,'r+') as file:
							#load json file to file_data
							file_data = json.load(file)
							#for each item in file
							for item in file:
								#set text_content to set file
								text_content = str(item)
								#in file data find variable ["ASIN"] and add data to selected row with method get product detail
								file_data["ASIN"].append(get_product_detail(response))
								#in file data find variable ["ASIN"] and add data to selected row with method get product review
								file_data["ASIN"].append(get_reviews(response))
							json.dump(file_data, file, indent = 4)
					#write result to text
					f.write(text_content + "\n")
			except Exception as e:
				print("Error", e)
	
		with open('temporary_search_result.json', 'w', encoding='utf-8') as jsonfile:
			json.dump(file_data, jsonfile, indent=4)
						



def get_reviews(response):
	#for store review

	#set selector to response text
	sel = Selector(text=response.text)
	#find the feature bullets
	reviews = []
	for review_element in sel.css("div.review-container"):  # Adjust this selector based on your HTML
					review = {
						"review_title": review_element.css("a.review-title ::text").get(),
						"review_text": review_element.css("span.review-text ::text").get(),
						"review_rating": review_element.css("i.review-rating ::text").get(),
							
					}
	reviews.append(review)

	return reviews

def get_product_detail(response):
	#for store review
	product_data_list = []
	#set selector to response text
	sel = Selector(text=response.text)
	#find the feature bullets
	feature_bullets = [bullet.strip() for bullet in sel.css("#feature-bullets li ::text").getall()]
	#find price
	if not price:
		price = sel.css('.a-price .a-offscreen ::text').get("")
		#add data column to product data list
	product_data_list.append({
		"stars": sel.css("i[data-hook=average-star-rating] ::text").get("").strip(),
		"rating_count": sel.css("div[data-hook=total-review-count] ::text").get("").strip(),
		"feature_bullets": feature_bullets,
	})
	return product_data_list


def clean_html(input):
    output = bleach.clean(str(input), tags=[], strip=True)
    output = str(output)
    return output


# def json_data_mock():
# 	json_file = open('sample.json')
# 	if json_file == None or json_file == []:
# 			print("result bad")
# 	else:
# 		parsed_json = json.load(json_file)
# 	return parsed_json

# def csv_json_mock():
# 	result = []
# 	with open('sample.json', 'r', encoding='utf-8') as json_file:
# 		if json_file == None:
# 			print("result bad")
# 		else:
# 			result = json.load(json_file)
# 	print("\t end amazon")
# 	return result


# def test_prod():
# 	result = []
# 	json_file = open('sample.json')
# 	if json_file == None or json_file == []:
# 			print("result bad")
# 	else:
# 			result = json.load(json_file)
# 			print(result)
# 	print("\t end amazon")
# 	json_file.close()

