import requests

# query = "car"

# j = requests.get("https://graph.facebook.com/search?access_token=" + token +  "&q=" + query + "&type=page")
# t = j.text
# print(t)

# from facepy import GraphAPI
# token = "EAALXhdY6tlsBANC8W7pEobygbxmnCvXqV2M0pZCkeLP2bwqOR0ciWKcmCDDQN1UzbjkJnw7jD4KT9ZCRiW3s0t1TS60r0kInFcULU7GFrYycLsczOvsh6n1staNdKMV3M2rXiwD2mmuM4N6cS2aV2qcjd6mrUB2cYu6QgdoPEqpj0fZAHRfUL62F83l680YZBr6vjdeQbQZDZD"
# # Initialize the Graph API with a valid access token (optional,
# # but will allow you to do all sorts of fun stuff).
# graph = GraphAPI(token)
#
# # Get my latest posts
# j = graph.get('me')
# print(j)

import facebook_scraper as fs
# for post in get_posts('car', pages=10 , page_limit=100):
#     print(post['text'][:50])
POST_ID = "pfbid02NsuAiBU9o1ouwBrw1vYAQ7khcVXvz8F8zMvkVat9UJ6uiwdgojgddQRLpXcVBqYbl"

# number of comments to download -- set this to True to download all comments
MAX_COMMENTS = 100

# get the post (this gives a generator)
gen = fs.get_posts(
    post_urls=[POST_ID],
    options={"comments": MAX_COMMENTS, "progress": True}
)

# take 1st element of the generator which is the post we requested
post = next(gen)

# extract the comments part
comments = post['comments_full']

# process comments as you want...
for comment in comments:

    # e.g. ...print them
    print(comment)

    # e.g. ...get the replies for them
    for reply in comment['replies']:
        print(' ', reply)