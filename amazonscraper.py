API_KEY = ''
import requests
search_query = input("Enter your search query for amazon: ")
payload = {'api_key': '', 'us': 'amazon.com','query': search_query}
r = requests.get('https://api.scraperapi.com/structured/amazon/search', params=payload)
print(r.text)

with open("response_az.txt", "w") as f:
	f.write(str(r))

with open("response_az_content.txt", "w") as f:
	f.write(str(r.content))