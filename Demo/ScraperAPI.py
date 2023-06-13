import requests
import pandas as pd

twitter_data = []

payload = {
    'api_key': '',
    'query': 'sentiment analysis',
    'num': '100'
}
response = requests.get(
    'https://api.scraperapi.com/structured/twitter/search', params=payload)
data = response.json()

all_tweets = data['tweets']
for tweet in all_tweets:
    twitter_data.append({
        'ID': tweet['tweet_id'],
        'User': tweet["user"],
        'Tweet': tweet["text"],
        'URL': tweet["link"]
    })

df = pd.DataFrame(twitter_data)
df.to_json('scraped_tweets.json', orient='index')
print('Tweets exported to JSON')