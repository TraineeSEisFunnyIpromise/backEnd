import asyncio
from playwright.async_api import async_playwright
from Review_scraper.PWRAZscrape import search_review

from URLcleaner import urlcleaner
import csv
import json
URL = "https://www.amazon.com/s?k="
async def scrape_amazon(search_term, search_group):
    async with async_playwright() as p:
        if search_group != '':
            search = search_term + " for " + search_group

        browser = await p.chromium.connect_over_cdp("u@brd.superproxy.io:9222")
        page = await browser.new_page()
        await page.goto(URL)

        # Enter search term and get product data
        await page.fill("#twotabsearchtextbox", search)
        await page.press("#twotabsearchtextbox", "Enter")
        await page.wait_for_selector(".s-card-container")
        products = await parse_results(page)

        # For each product, scrape reviews and add them to the product data
        for product in products:
            asin = urlcleaner(product["url"])  # Function to extract ASIN from URL
            reviews = await search_review(asin)  # Scrape reviews using your review scraping function
            product["reviews"] = reviews  # Add reviews to the product data

        # Save the combined data
        await save_data(products)
        await browser.close()


async def parse_results(page):
    return await page.evaluate('''() => {
        return Array.from(document.querySelectorAll(".s-card-container")).map(el => {
            return {
                url: el.querySelector("a")?.getAttribute("href"),
                title: el.querySelector("h2 span")?.innerText,
                price: el.querySelector(".a-price > .a-offscreen")?.innerText,
                rating: el.querySelector(".a-icon-alt")?.innerText,
            };
        });
    }''')

async def save_data(data):
        filename = 'test10.csv'
        print("Jsoning data")
        data_json = json.dumps(data)
        count = 0
        for item in data:
            count += 1
            #finding URL, Title and Price
            print(f"Found product: {item['url'],item['title']}, {item['price']}, {item['rating']}")
            print('Response Code: ',)
            print('Response Scraped Body: ', data_json)
            with open(filename, "w") as outfile:
                outfile.write(data_json)

# when want to use it independently
# search_term = input("Please type some input: ")
# from reqandscrape.requestsender.chatgptreqsender import receiveinput
# search_term = "electic fan for student "
# asyncio.run(scrape_amazon(search_term))

