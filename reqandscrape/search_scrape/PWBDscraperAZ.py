import asyncio
from playwright.async_api import async_playwright
import csv
import json
URL = "https://www.shopee.com/search?keyword="

async def scrape_amazon(search_term):
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("@brd.superproxy.io:9222")
        print("Connected to browser...")
        print("Sending requests via residential proxies...")

        # Create a new page
        page = await browser.new_page()
        page.set_default_navigation_timeout(2 * 60 * 1000)

        # Go to Amazon.com
        await page.goto(URL, wait_until="domcontentloaded")
        print("Navigated to home page")
        await page.wait_for_selector("#twotabsearchtextbox", timeout=30000)

        # Type a search term in the search input
        print("Search phrase")
        await page.fill("#twotabsearchtextbox", search_term)
        print("Entered search term")
        await page.press("#twotabsearchtextbox", "Enter")

        # Wait for the products to load
        await page.wait_for_selector(".s-card-container", timeout=30000)
        print("Products loaded, parsing...")

        data = await parse_results(page)
        save_data(data)

        await browser.close()
        return data


async def parse_results(page):
    return await page.evaluate('''() => {
        return Array.from(document.querySelectorAll(".s-card-container")).map(el => {
            return {
                url: el.querySelector("a")?.getAttribute("href"),
                title: el.querySelector("h2 span")?.innerText,
                price: el.querySelector(".a-price > .a-offscreen")?.innerText,
            };
        });
    }''')

async def save_data(data):
    
        filename = 'test1.csv'
        print("Jsoning data")
        data_json = json.dumps(data)
        count = 0
        for item in data:
            count += 1
            #finding URL, Title and Price
            print(f"Found product: {item['url'],item['title']}, {item['price']}")
            print('Response Code: ',)
            print('Response Scraped Body: ', data_json)
            with open(filename, "w") as outfile:
                outfile.write(data_json)

async def save_scrape_data(data):
        print("Jsoning data")
        data_json = json.dumps(data)
        response_data = []
        count = 0
        for item in data:
            count += 1
            #finding URL, Title and Price
            response_data = item['url'],item['title'], item['price']
        return response_data

async def save_scrape_test_data():
        data = ""
        data_json = json.dumps(data)
        response_data = []
        count = 0
        for item in data_json:
            count += 1
            #finding URL, Title and Price
            response_data = item['url'],item['title'], item['price']
        return response_data

# when want to use it independently
search_term = input("Please type some input: ")
asyncio.run(scrape_amazon(search_term))

