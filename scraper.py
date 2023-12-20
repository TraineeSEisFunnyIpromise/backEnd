import scrapy
from scrapy.crawler import CrawlerProcess
from amazon import AmazonProductSpider  # Import your spider

def main():
    keyword = input("Enter search keyword: ")
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (compatible; MyScraper/1.0; +http://example.com)'
    })
    process.crawl(AmazonProductSpider, keyword=keyword)  # Pass keyword as argument
    process.start()

if __name__ == '__main__':
    main()