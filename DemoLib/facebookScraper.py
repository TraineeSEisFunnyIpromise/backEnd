#import Facebook_scraper class from facebook_page_scraper
from facebook_page_scraper import Facebook_scraper

#instantiate the Facebook_scraper class

page_name = "metaai"
posts_count = 10
browser = "firefox"
timeout = 600 #600 seconds
headless = True
meta_ai = Facebook_scraper(page_name, posts_count, browser, timeout=timeout, headless=headless)

print(meta_ai)