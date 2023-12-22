import scrapy
from scrapy.crawler import CrawlerProcess
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
    name = 'amazonspider'
    # custom_feed = {
    #     "/home/user/documents/items.json": {
    #         "format": "json",
    #         "indent": 4,
    #     }
    # }

    def update_settings(self):
        self.crawler.settings.set('USER_AGENT','Mozilla/5.0 (compatible; MyScraper/1.0; +http://google.com)')
    # def update_settings(cls, settings):
    #     super().update_settings(settings)
    #     settings.set(priority="spider")


    def __init__(self, keyword):
        self.update_settings()
        self.start_urls = f'https://www.amazon.com/s?k='.format(keyword)
        # Yield the product IDs as Scrapy items
        product_ids = keyword.css('[data-asin]::attr(data-asin)').getall()
        for product_id in product_ids:
            yield {
                'product_id': product_id
            }



