"""
Download comments for a public Facebook post.
"""

import facebook_scraper as fs

# get POST_ID from the URL of the post which can have the following structure:
# https://www.facebook.com/USER/posts/POST_ID
# https://www.facebook.com/groups/GROUP_ID/posts/POST_ID
POST_ID = "pfbid02NsuAiBU9o1ouwBrw1vYAQ7khcVXvz8F8zMvkVat9UJ6uiwdgojgddQRLpXcVBqYbl"
username = ''
password = ''
#set up proxy
proxy_options = f'http://{username}:{password}@gate.smartproxy.com:7000'
fs.set_proxy(proxy_options,True)

# number of comments to download -- set this to True to download all comments
MAX_COMMENTS = 10


# gen = fs.get_posts(
#     post_urls=[POST_ID],
#     options={"comments": MAX_COMMENTS, "progress": True}
# )

# gen = fs.get_posts_by_search(
#     'football',
#     options={"comments": MAX_COMMENTS, "progress": True}
# )


# get the post (this gives a generator)
#๊username and password
#
#
gen = fs.get_posts_by_search(
    'football',credentials=['',''],
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

# def searching_post(input_raw):
#     result_a = fs.get_posts_by_search(input_raw)
#     something = result_a
#     return something


