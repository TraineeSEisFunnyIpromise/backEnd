import scrapy

# class AmazonSpider(scrapy.Spider):
#     name = 'amazon'

#     def parse(self, response):
#         # Extract product IDs from search results
#         product_ids = response.css('[data-asin]::attr(data-asin)').getall()

        # # Yield the product IDs as Scrapy items
        # for product_id in product_ids:
        #     yield {
        #         'product_id': product_id
        #     }

class AmazonSpider(scrapy.Spider):
    name = 'amazon'

    def __init__(self, response, keyword):
        self.start_urls = [f'https://www.amazon.com/s?k={keyword}']  # Use keyword in start URL
        # ... rest of your spider code
        # Yield the product IDs as Scrapy items
        product_ids = response.css('[data-asin]::attr(data-asin)').getall()
        for product_id in product_ids:
            yield {
                'product_id': product_id
            }