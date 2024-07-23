import asyncio
from playwright.async_api import async_playwright
import csv
import json
URL = "https://www.shopee.com/search?keyword="
search_term = input("please type some input: ")

async def run():
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
        await page.wait_for_selector("#", timeout=30000)
        
        # Type a search term in the search input
        print("search phrase")
        await page.fill("#", search_term)
        print("Entered search term")
        await page.press("#", "Enter")
        
        # Wait for the products to load
        await page.wait_for_selector(".", timeout=30000)
        print("Products loaded, parsing...")
        
        data = await parse_results(page)
        filename = 'test2.csv'
        print("Jsoning data")
        data_json = json.dumps(data)
        count = 0
        for item in data:
            count += 1
            print(f"Found product: {item['url'],item['title']}, {item['price']}")
            print('Response Code: ',)
            print('Response Scraped Body: ', data_json)
            with open(filename, "w") as outfile:
                outfile.write(data_json)
        await browser.close()

async def parse_results(page):
    return await page.evaluate('''() => {
        
        return Array.from(document.querySelectorAll(".")).map(el => {
            return {
                url: el.querySelector("")?.getAttribute(""),
                title: el.querySelector("")?.innerText,
                price: el.querySelector("")?.innerText,
            };
        });
    }''')

asyncio.run(run())
