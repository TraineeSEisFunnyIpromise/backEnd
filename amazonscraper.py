from urllib.parse import urljoin
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import lxml



# Function to extract Product Title
def get_title(soup):

    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id":'productTitle'})
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

# Function to extract Product Price
def get_price(soup):

    try:
        price = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()

    except AttributeError:

        try:
            # If there is some deal price
            price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()

        except:
            price = ""

    return price

# Function to extract Product Rating
def get_rating(soup):
    print("get Rating")
    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
    
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""	

    return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
    print("get review")
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""	

    return review_count

# Function to extract Availability Status
def get_availability(soup):
    print("check avaliability")
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available"	

    return available

if __name__ == '__main__':

    # yup
    #xpath //*[@id="anonCarousel2"]/ol/li[1]/div/div/div/span/div/div/div[2]/div[2]/h2
    search_query = input("Enter your search query for amazon: ")
    # The webpage URL
    URL = 'https://www.amazon.com/s?' + search_query
    #payload for search
    payload = {'api_key': '','url': URL ,'us': 'amazon.com', 'device_type': 'desktop'}
    #payload for the looping search product
    p_payload = {'api_key': '','us': 'amazon.com', 'device_type': 'desktop'}
    # HTTP Request
    webpage = requests.get('https://api.scraperapi.com/',payload)
    
    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")
    print(soup)
    # Fetch links as List of Tag Objects
    links = soup.find_all(attrs={'class':'a-carousel-card'})

    # Store the links
    links_list = []

    # Loop for extracting links from Tag Objects
    for link in links:
            links_list.append(link.get('href'))

    d = {"title":[]}
    # d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[]}
    
    # Loop for extracting product details from each link 
    for link in links_list:
        
        new_webpage = requests.get("https://api.scraperapi.com/"+'https://www.amazon.com'+ link,p_payload)

        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        # Function calls to display all necessary product information
        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['rating'].append(get_rating(new_soup))
        d['reviews'].append(get_review_count(new_soup))
        d['availability'].append(get_availability(new_soup))

    
    # amazon_df = pd.DataFrame.from_dict(d)
    # amazon_df['title'].replace('', np.nan, inplace=True)
    # amazon_df = amazon_df.dropna(subset=['title'])
    # amazon_df.to_csv("amazon_data.csv", header=True, index=False)