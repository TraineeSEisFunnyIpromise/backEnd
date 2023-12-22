# -*- coding: utf-8 -*-
import scrapy
from amazon.amazon.items import AmazonItem
from scrapy.crawler import CrawlerProcess

class AmazonProductSpider(scrapy.Spider):
  name = "AmazonDeals"
  allowed_domains = ["amazon.com"]
  start_urls = []
  def parse(self, response):
   items = AmazonItem()
   title = response.xpath('//h1[@id="title"]/span/text()').extract()
   sale_price = response.xpath('//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()').extract()
   category = response.xpath('//a[@class="a-link-normal a-color-tertiary"]/text()').extract()
   availability = response.xpath('//div[@id="availability"]//text()').extract()
   items['product_name'] = ''.join(title).strip()
   items['product_sale_price'] = ''.join(sale_price).strip()
   items['product_category'] = ','.join(map(lambda x: x.strip(), category)).strip()
   items['product_availability'] = ''.join(availability).strip()
   yield items


def __init__(self, keyword):
   keyword = input("Enter search keyword: ")
   self.start_urls = [f'https://www.amazon.com/s?k={keyword}']

def main():
    keyword = input("Enter search keyword: ")
    process.crawl(AmazonProductSpider, keyword=keyword)
    process.start()

process = CrawlerProcess(settings={
    'FEED_URI':'Car.csv',
    'FEED_FORMAT':'csv'
})

if __name__ == '__main__':
   main()
   