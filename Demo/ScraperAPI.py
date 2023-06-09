import requests
url = 'https://www.google.com'
api_key = ""
base_url = "https://api.scraperapi.com?api_key="+api_key+"&url="
request_url = base_url + url
response = requests.get(request_url)
content = response.text

print(content)
