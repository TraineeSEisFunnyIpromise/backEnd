
from seleniumwire import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
#All Spent
# SCRAPEOPS_API_KEY = ''
#still have left
## Define OutsourceAPI Proxy Port Endpoint 
username = ''
password = ''
proxy_options = {
    'proxy': {
        'http': f'http://{username}:{password}@gate.smartproxy.com:7000',
        'https': f'https://{username}:{password}@gate.smartproxy.com:7000',
        'no_proxy': 'localhost:127.0.0.1'
    },
    'prefs': {
        'profile.managed_default_content_settings.images': 2,
        'profile.default_content_setting_values.javascript': 2
    }
}

## Set Up Selenium Chrome driver

# Initialize ChromeOptions
options = webdriver.ChromeOptions()

# Set preferences to block images and JavaScript
prefs = {
    "profile.managed_default_content_settings.images": 2,
    "profile.default_content_setting_values.javascript": 2
}
options.add_experimental_option("prefs", prefs)


chromedriver_autoinstaller.install() 
driver = webdriver.Chrome(seleniumwire_options=proxy_options)
#waiting method prevent get caught
wait = WebDriverWait(driver, 10)
## Send Request Using ScrapeOps Proxy
driver.get('https://www.amazon.com/')

## Retrieve HTML Response
html_response = driver.page_source

## Extract Data From HTML
searchkeyword='toycar'
soup = BeautifulSoup(html_response, "html.parser")
search_input = driver.find_element(By.XPATH,'/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[2]/div[1]/input')
search_input.send_keys(searchkeyword)
search_btn = driver.find_element(By.XPATH,'/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[3]/div/span/input')
search_btn.click()
wait.until(EC.url_changes('https://www.amazon.com/'))
h1_text = soup.find_all('a',attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
#element target
#<a class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"
print("finding a to class")
print(h1_text)
print("-----------------------------------------------")
print("printall")
print(soup)
