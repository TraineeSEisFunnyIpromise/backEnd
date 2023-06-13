import tweepy

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
tweets = []
username = 'twitter_username'
count = 20
# Get the tweets
try:
    # Creation of query method using parameters
    tweets = api.user_timeline(id=username, count=count)
    # Pulling information from tweets iterable object
    for tweet in tweets:
        print(tweet.text)
except tweepy.TweepError as e:
    print("Error : " + str(e))