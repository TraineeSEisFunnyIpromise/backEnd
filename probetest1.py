import sys
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
if sys.version_info[0]==3:
    import urllib.request
    import random
    username = ''
    password = ''
    port = 22225
    session_id = random.random()
    super_proxy_url = ('http://%s-session-%s:%s@brd.superproxy.io:%d' %
        (username, session_id, password, port))
    proxy_handler = urllib.request.ProxyHandler({
        'http': super_proxy_url,
        'https': super_proxy_url,
    })
    opener = urllib.request.build_opener(proxy_handler)
    print('Performing request')
    print(opener.open('http://www.google.com/search?q=pizza').read())