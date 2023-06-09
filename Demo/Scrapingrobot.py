import requests

url = 'https://api.scrapingrobot.com/?token='
headers = {
    'accept': 'application/json',
    'content-type': 'application/json'
}
data = {
    'url': 'https://www.google.com',
    'module': 'GoogleScraper',
    "params": {
        "query": "pizza",
        "proxyCountry": "TH"
    }
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
