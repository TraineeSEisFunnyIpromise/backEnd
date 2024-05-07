from urllib.parse import urljoin
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from lxml import etree



# Function to extract Product Title
# def get_title(soup):

#     try:
#         # Outer Tag Object
#         title = soup.find("span", attrs={"id":'productTitle'})
        
#         # Inner NavigatableString Object
#         title_value = title.text

#         # Title as a string value
#         title_string = title_value.strip()

#     except AttributeError:
#         title_string = ""

#     return title_string


if __name__ == '__main__':

    # yup
    #xpath //*[@id="anonCarousel2"]/ol/li[1]/div/div/div/span/div/div/div[2]/div[2]/h2
    search_query = input("Enter your search query for amazon: ")
    # The webpage URL
    URL = 'https://www.amazon.com/s?' + search_query
    #payload for search
    payload = {'api_key': 'b9c4d81385407a68cbfc35e121f2cea9','url': URL ,'us': 'amazon.com', 'device_type': 'desktop'}
    #payload for the looping search product
    
    # HTTP Request
    webpage = requests.get('https://api.scraperapi.com/',payload)
    
    # Soup Object containing all data
    soup = BeautifulSoup(webpage.text, "html.parser")
    print("---------------------begin soup print---------------------------")
    print(soup)
    print("-----------------------end soup print---------------------------")
    l=[]
    o={}
    # Fetch links as List of Tag Objects
    # target <span class="a-size-base-plus a-color-base a-text-normal"
    #please amazon search is so hard bro like wtf
    try:
        o["title"]=soup.find('span',{'class':'a-size-base-plus a-color-base a-text-normal'}).text.strip()
        with open("response_az_content.txt", "wb") as f:
            f.write(o)
    except:
        o["title"]=None
    