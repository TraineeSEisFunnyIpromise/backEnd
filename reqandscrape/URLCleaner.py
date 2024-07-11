import regex as re
import json

# Opening JSON file
with open('sample.json', 'r') as openfile:
 
    # Reading from json file
    json_object = json.load(openfile)

for line in json_object:
    url = line.get("url")
    asin = re.search(r'/[dg]p/([^/]+)', url, flags=re.IGNORECASE)
    if asin:
        if asin.re.search():
            print("something")