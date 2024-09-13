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
import unicodedata
from selenium import webdriver
from seleniumwire import webdriver as webdriver_wire
from bs4 import BeautifulSoup

# Options for Chrome driver
# Navigate to the website
def amazon_scrape(inputkeyword):
	options = webdriver.ChromeOptions()
	options.add_argument('--incognito')  # Open in incognito mode
	options.add_argument('--disable-extensions')  # Disable extensions
	options.add_argument('--disable-gpu')  # Disable GPU
	options.add_argument('start-maximized')  # Start maximized
	options.add_argument('disable-infobars')  # Disable infobars
	options.add_argument('--headless')  # headless

	# Replace with your proxy server URL
	proxy_server_url = ""
	options.add_argument(f'--proxy-server={proxy_server_url}')
	# Create a Selenium Wire driver
	driver = webdriver_wire.Chrome(options=options)
	driver.get("https://www.amazon.com")

	# Log network requests after navigation
	for request in driver.requests:
			print(f"Request: {request.method} {request.url}")  # Inspect requests

	driver.implicitly_wait(5)

	keyword = str(inputkeyword)
	search = driver.find_element(By.ID, 'twotabsearchtextbox')
	search.send_keys(keyword)

	# click search button
	driver.implicitly_wait(1)
	search_button = driver.find_element(By.ID, 'nav-search-submit-button')
	search_button.click()

	driver.implicitly_wait(5) 

	while True:
			try:
					#class="s-pagination-item s-pagination-button"
					driver.implicitly_wait(5)
					next_button = driver.find_element(By.CLASS_NAME, "s-pagination-item s-pagination-button")
					next_button.click()
			except (NoSuchElementException, TimeoutException):
					break  # If the "Next" button is not found, assume it's the last page

	content = driver.page_source
	soup = BeautifulSoup(content, 'html.parser')
	items = soup.findAll('div', 'sg-col-inner')
	item_sorting(items)
	with open("raw_result.txt", "w",encoding="utf-8") as f:
			for item in items:
					text_content = str(item)
					json_data = json.dumps(text_content, indent=4)
					f.write(json_data + "\n")
	#set data from search
	#review scraping begin

	# end process quit driver
	driver.quit()

# def review_scrape():
# 	return

# def item_sorting_review(items):
# 	return

def item_sorting(items):
	product_asin = []
	product_name = []
	product_price = []
	product_ratings = []
	product_ratings_num = []
	product_link = []
	for item in items:
			# find name
			#class="a-size-base-plus a-color-base a-text-normal"
			name = item.find_element(By.XPATH, './/span[@class="a-size-base-plus a-color-base a-text-normal"]')
			product_name.append(name.text) 

			# find ASIN number 
			data_asin = item.get_attribute("data-asin")
			product_asin.append(data_asin)

			# find price
			whole_price = item.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
			fraction_price = item.find_elements(By.XPATH, './/span[@class="a-price-fraction"]')
			
			if whole_price != [] and fraction_price != []:
					price = '.'.join([whole_price[0].text, fraction_price[0].text])
			else:
					price = 0
			product_price.append(price)

			# find ratings box
			#<class="a-icon a-icon-star-small a-star-small-4-5 aok-align-bottom">
			ratings_box = item.find_elements(By.XPATH, './/div[@class="a-row a-size-small"]/span')

			# find ratings and ratings_num
			if ratings_box != []:
					ratings = ratings_box[0].get_attribute('aria-label')
					ratings_num = ratings_box[1].get_attribute('aria-label')
			else:
					ratings, ratings_num = 0, 0
			
			product_ratings.append(ratings)
			product_ratings_num.append(str(ratings_num))
			
			# find 
			#class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal">
			link = item.find_element(By.XPATH, './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]').get_attribute("href")
			product_link.append(link)
	save_data_csv(product_name, product_asin, product_price, product_ratings, product_ratings_num, product_link)


def save_data_csv(product_name, product_asin, product_price, product_ratings, product_ratings_num, product_link):
	data = []
	data.append([product_name, product_asin, product_price, product_ratings, product_ratings_num, product_link])
	# Save data to CSV file
	with open('search_result_recent.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(['Product Name', 'ASIN', 'Price', 'Ratings', 'Ratings Num', 'Link'])  # Write header row
			writer.writerows(data)
	# to check data scraped

