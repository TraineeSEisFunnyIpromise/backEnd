from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time


# Initialize the Chrome WebDriver
#C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
#F:\Webdriver\chromedriver-win64\chromedriver.exe
s = Service('F:\Webdriver\chromedriver-win64\chromedriver.exe')
driver = webdriver.Chrome(service=s)

# Open Google
driver.get("http://www.google.com")

# Find the search box element and enter a query
search_box = driver.find_element(By.NAME,"q")
search_box.send_keys("Selenium Python tutorial")

# Perform the search
search_box.send_keys(Keys.RETURN)

# Wait for the search results to load
time.sleep(5)

# Print the title of the current page
print(driver.title)

# Close the browser
driver.quit()