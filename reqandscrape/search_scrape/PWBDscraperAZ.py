

#import stuff for selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException 
import csv,random,json
from selenium import webdriver
from seleniumwire import webdriver as webdriver_wire
from bs4 import BeautifulSoup
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
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
				print("\tOpen amazon page")
				driver.get("https://amazon.com")

				#wait for 5 second
				driver.implicitly_wait(500)
				#<input autocomplete="off" spellcheck="false" placeholder="Type characters" 
				# id="captchacharacters" name="field-keywords" class="a-span12" 
				# autocapitalize="off" autocorrect="off" type="text">

				#merge word
				print("\tWait time out 120")
				#finding search box
				driver.set_page_load_timeout(120)
				search = driver.find_element(By.ID, 'twotabsearchtextbox')
				#set condition if detected abandon task
				search.send_keys(keyword)
					# click search button
				driver.implicitly_wait(2)
				print("\tSubmit search key")
				search_button = driver.find_element(By.ID, 'nav-search-submit-button')

				# if(driver.find_element(By.ID,'captchacharacters') == True):
				# 	driver.quit()
				# 	return "detected capcha abandon task"
				#dump old data 
				print("\tWrite temp file")
				with open('temporary_search_result.json', 'w+', encoding='utf-8') as jsonfile:
						json.dump([], jsonfile)
				
				search_button.click()
				wait_count = 0
				page_limit = 0
				driver.implicitly_wait(800) 
				print("before looping")
				while page_limit <= 0:
					print("looping")
					time.sleep(8+ int(random.randrange(5)))  
					try:
						print("\tStarting")
						# Wait for the "Next" button to be clickable
						print("\tNext button detection")
						next_button = WebDriverWait(driver, 10).until(
							EC.element_to_be_clickable((By.XPATH, "//a[text()='Next']"))
						)
						# Wait for the "Next" button to be clickable MUST HAPPEN BEFORE WAITING
						print("\tSleeping")	
						#Wating for 10 seconds...MUST HAPPEN AFTER BUTTON FOUND
						time.sleep(8+ int(random.randrange(5)))
						print("\tScraping")
						# Scrape the page source after the list is populated
						content = driver.page_source
						soup = BeautifulSoup(content, 'html.parser')
						items = soup.find_all('div', attrs={'data-component-type': 's-search-result'})#this method work in test
						print("item sorting")
                                          
						with open("raw_result.txt", "w+",encoding="utf-8") as f:
						#open temporary search result.json file
					#write result to text
							f.write(str(items) + "\n")
						print("before click button")
						item_sorting(items)
						
						# Click the "Next" button to go to the next page
						next_button.click()
						
						# Update the page limit counter
						page_limit = page_limit +  1
						print("page limit ",page_limit)
						
						# Optional: wait between pages to prevent hitting Amazon too quickly
						time.sleep(8+ int(random.randrange(5)))  
					except Exception as e:
						print("Exception :",str(e))
						error_message = str(e)  # Get the error message as a string

						if "target window already closed" in error_message and "web view not found" in error_message:
							break
						
						wait_count += 1
						if wait_count >= 120 // 2:  # Check after half of max wait time
							print(wait_count)
							print("Error: Encountered delays for too long")
							driver.quit()
							# break  # Exit the loop if exceeded maximum wait attempts
				print("end of loop")


					#setting up ASIN
				print("setting up asin")

				print("quit old driver")
				driver.quit()
				# print(result = json.load(open('temporary_search_result.json', 'r')) if open('temporary_search_result.json', 'r') else None )

				asin_set = get_asin()
				# begin product scraping
				print("check asin for product scraping")
				if isinstance(asin_set, list) and asin_set:
						print("scraping")
						print("setting up new driver")
						print("scraping product")
						try:
							scrape_amazon_product(asin_set)
						except Exception as e:
							print(f"An error occurred while scraping product {e}")
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

			
				print("\t count and add the ID")
				with open('temporary_search_result.json', 'r', encoding='utf-8') as json_file:
					try:
						data = json.load(json_file)
					except json.JSONDecodeError as e:
						print(f"Error loading JSON: {e}")
						data = []  # Initialize an empty list in case of errors

					id_count = 1
					for item in data:
						if item is not None:
							if 'id' not in item:
								item['id'] = id_count
								id_count += 1
								print(item)

				print("\t finalized data")
				with open('temporary_search_result.json', 'w', encoding='utf-8') as json_file:
					json.dump(data, json_file, ensure_ascii=False, indent=4) 
                                   

				result = json.load(open('temporary_search_result.json', 'r',encoding='utf-8')) if open('temporary_search_result.json', 'r') else None 
				# print("\t sending")
				if result != None:
					print("\t Success")
					print(result)
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

    for item_soup in items:
        # item_soup = BeautifulSoup(item_text, 'html.parser')  # Create BeautifulSoup object

        try:
            product_name = item_soup.find('h2', class_="a-size-medium a-spacing-none a-color-base a-text-normal").text.strip() 
        except AttributeError:
            product_name = None

        try:
            product_price = item_soup.find('span', class_='a-price-whole').text.strip()
        except AttributeError:
            product_price = None

        try:
            product_ratings = item_soup.find('span', class_='a-icon-alt').text.strip()
        except AttributeError:
            product_ratings = None

        try:
            product_link = item_soup.find("a", class_='a-link-normal s-no-outline')['href'] 
        except (AttributeError, KeyError):
            product_link = None

        product_asin = urlcleaner(product_link) if product_link else None 

        # Collect the data only if the product name exists
        if product_name:
            product_data = {
                "title": str(product_name),
                "price": str(product_price),
                "rating": str(product_ratings),
                "asin": str(product_asin),
                "url": str(product_link)
            }
            data.append(product_data)

    with open('temporary_search_result.json', 'w', encoding='utf-8') as jsonfile:
      json.dump(data, jsonfile, indent=4)

        


def get_asin():
    data = []
    with open('temporary_search_result.json', 'r+') as jsonfile:
        if jsonfile:
            json_data = json.load(jsonfile)
            for asin in json_data:
                if asin['asin']!=None:
                    data.append(asin['asin'])
                else:
                    print("Empty ASIN found.")
    print("asin data")
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
    return clean_url.group(0) if clean_url else None
# #----------------review scraping---------------------

def scrape_amazon_product(asin, json_file='temporary_search_result.json'):
    file_data = None
    print("Before processing ASINs")

    for i in asin:
        if (i is not None) and (i != 'None'):
            print("Processing ASIN:", i)
            url = f'https://www.amazon.com/dp/{i}'

            try:
                response = requests.get(str(url), proxies={'http': proxy, 'https': proxy})
                print("Proxy set")
                time.sleep(3)

                if response.status_code == 200:
                    # Load or create JSON data
                    print("Loading JSON data")
                    with open(json_file, 'r+') as file:
                        try:
                            file_data = json.load(file)
                        except json.JSONDecodeError:
                            file_data = {}

                    # Extract product details
                    result_detail = get_product_detail(response)
                    result_review = get_reviews(response)  # Add this line
                    print("Extracted product details asin :", i)
                    print("Extracted product reviews asin :", i)

                    # Find matching object in JSON (assuming unique ASINs)
                    matching_object = None
                    for item in file_data:
                        if item.get('asin') == i:  # Use get() for potential missing key
                            matching_object = item
                            break  # Exit loop once a match is found (assuming unique ASINs)

                    if matching_object:
                        # Add result_detail and result_review to matching object
                        matching_object['details'] = result_detail 
                        matching_object['reviews'] = result_review 
                        print("Appended details and reviews to matching object to asin : ", i)
                    else:
                        print("No matching object found for ASIN:", i)

                    # Save updated JSON data
                    with open(json_file, 'w') as file: 
                        json.dump(file_data, file, indent=4)

            except Exception as e:
                print("Error:", e)
						
						


def get_reviews(response):

    if response.status_code != 200:
    # print an error message with the status code
        print(f"An error occurred with status {response.status_code}")
    else:
        # get the page html content
        html_content = response.text
        # parse the html content using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")


        # find all elements with class name "review-title"
        review_titles = soup.find_all("a", class_="review-title")
        titles_list = [title.text.replace("5.0 out of 5 stars\n", "").strip() for title in review_titles]
        
        # find all elements with class name "review-text-content"
        review_texts = soup.find_all("span", class_="review-text")
        review_texts_list = [text.get_text(separator="\n").strip() for text in review_texts]


        # find all elements with class name "review-rating"
        review_ratings = soup.find_all("i", class_="review-rating")
        review_ratings_list = [rating.text.strip() for rating in review_ratings]


        # create a dictionary to store the review details
        reviews = {

            "Review Titles": titles_list,
            "Review Texts": review_texts_list,
            "Review Star Ratings": review_ratings_list,
        }

        # print the dictionary
    return reviews

def get_product_detail(response):
		#for store review
		product_data_list = []
		#set selector to response text
		sel = Selector(text=response.text)
		#find the feature bullets
		feature_bullets = [bullet.strip() for bullet in sel.css("#feature-bullets li ::text").getall()]

		product_data_list.append({
					# "stars": stars,
					# "rating_count": rating_count,
					"description": feature_bullets,
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

