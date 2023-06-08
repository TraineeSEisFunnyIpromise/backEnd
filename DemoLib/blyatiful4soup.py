import requests
from bs4 import BeautifulSoup

# URL of the Facebook page or post you want to scrape
url = "https://www.facebook.com/hashtag/gamingdose"

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object from the response content
soup = BeautifulSoup(response.content, "html.parser")

# Find all the tags with the desired class or attribute
tags = soup.find_all("div", class_="_6s5d _71pn system-fonts--body segoe")

# Extract the information you need from the tags
for tag in tags:
    # Process the tag or extract specific data
    # Example: print the text content of each tag
    print(tag.text)
