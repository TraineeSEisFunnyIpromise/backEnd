import scrapy
from amazon.amazon.items import AmazonItem  # Adjust path if needed
from scrapy.crawler import CrawlerProcess
#educational purpose only
class AmazonProductSpider(scrapy.Spider):
    name = "AmazonDeals"
    # allowed_domains = ["amazon.com"]
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
