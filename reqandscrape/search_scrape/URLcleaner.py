import regex as re
import json

# Opening JSON file a URL cleaner
with open('sample.json', 'r') as openfile:
 
    # Reading from json file
    json_object = json.load(openfile)
for line in json_object:
    url = line.get("url")
    asin = re.search(r'/[dg]p/([^/]+)', json_object, flags=re.IGNORECASE)
    if asin:
        print(asin.group(1))

#output
