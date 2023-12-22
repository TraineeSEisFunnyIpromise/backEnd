import scrapy
from amazon.amazon.items import AmazonItem  # Adjust path if needed
from scrapy.crawler import CrawlerProcess
#educational purpose only
class AmazonProductSpider(scrapy.Spider):
    name = "AmazonDeals"
    # allowed_domains = ["amazon.com"]
    # custom_settings = {
    # 'DOWNLOADER_MIDDLEWARES' : 
    # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware' : None,
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    # 'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    # 'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
    # ## settings.py
    # 'FAKEUSERAGENT_PROVIDERS' = 
    #     'scrapy_fake_useragent.providers.FakeUserAgentProvider',  # This is the first provider we'll try
    #     'scrapy_fake_useragent.providers.FakerProvider',  # If FakeUserAgentProvider fails, we'll use faker to generate a user-agent string for us
    #     'scrapy_fake_useragent.providers.FixedUserAgentProvider',  # Fall back to USER_AGENT value
    # }

    def parse(self, response):
        items = AmazonItem()
        items['product_name'] = response.css(".a-size-medium a-color-base a-text-normal::text").get()
        yield items

        next_page = response.css("li.a-last a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def __init__(self, keyword):

        self.start_urls = [f'https://www.lazada.co.th/catalog/?q={keyword}']


def main():
    keyword = input("Enter search keyword: ")
    process.crawl(AmazonProductSpider, keyword=keyword)
    process.start()

process = CrawlerProcess(settings={
    'FEED_URI': 'Car.csv',
    'FEED_FORMAT': 'csv'
})

if __name__ == '__main__':
    main()
