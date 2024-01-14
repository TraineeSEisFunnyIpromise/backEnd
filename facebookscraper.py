import requests
from urllib.parse import urlencode
search_query = input("Enter your search query for facebook: ")
proxy_params = {
      'api_key': '',
      'url': 'https://www.facebook.com/search/top/?q={search_query}',
      'render_js': True,
  }

response = requests.get(
  url='https://proxy.scrapeops.io/v1/',
  params=urlencode(proxy_params),
  timeout=120,
)

print('Body: ', response.content)


with open("response.txt", "w") as f:
	f.write(str(response))

with open("response_content.txt", "w") as f:
	f.write(str(response.content))

#target Xpath //*[@id="mount_0_0_x0"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]
#target jspath document.querySelector("#mount_0_0_x0 > div > div:nth-child(1) > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x9f619.x2lah0s.x1nhvcw1.x1qjc9v5.xozqiw3.x1q0g3np.x78zum5.x1iyjqo2.x1t2pt76.x1n2onr6.x1ja2u2z.x1h6rjhl > div.x9f619.x1n2onr6.x1ja2u2z.xdt5ytf.x193iq5w.xeuugli.x1r8uery.x1iyjqo2.xs83m0k.x78zum5.x1t2pt76")
#target Full xpath /html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]

#document.querySelector("#mount_0_0_x0 > div > div:nth-child(1) > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x9f619.x2lah0s.x1nhvcw1.x1qjc9v5.xozqiw3.x1q0g3np.x78zum5.x1iyjqo2.x1t2pt76.x1n2onr6.x1ja2u2z.x1h6rjhl > div.x9f619.x1n2onr6.x1ja2u2z.xdt5ytf.x193iq5w.xeuugli.x1r8uery.x1iyjqo2.xs83m0k.x78zum5.x1t2pt76 > div > div > div > div > div")
#/*[@id="mount_0_0_x0"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div
#/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div


# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#     custom_settings = {
#         'SCRAPEOPS_PROXY_SETTINGS': {'country': 'us'}
#     }

#     def start_requests(self):
#         urls = "https://www.facebook.com/search/results/?q=car"
#         for url in urls:
#             print("work")
#             yield scrapy.Request(url=url, callback=self.parse)

#     def parse(self, response):
#         posts = response.css('div.userContentWrapper')  # Adjust selector if needed
#         for post in posts[:20]:  # Target only the first 20 posts
#             yield {
#                 'title': post.css('h2.text_exposed_root a::text').get(),
#                 'description': post.css('div.text_exposed_root span::text').get(),
#                 'comments': post.css('ul.UFIList li div.UFICommentBody::text').getall(),  # Assuming comments are visible
#             }
#         # Follow pagination links (if applicable)
#         next_page = response.css('a.next::attr(href)').get()
#         if next_page:
#             yield response.follow(next_page, callback=self.parse)
