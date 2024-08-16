

# # Opening JSON file a URL cleaner
# def test_urlcleaner():
#     with open('sample.json', 'r') as openfile:
#         # Reading from json file
#         json_object = json.load(openfile)
#     for line in json_object:
#         url = line.get("url")
#         asin = re.search(r'/[dg]p/([^/]+)', json_object, flags=re.IGNORECASE)
#         if asin:
#             print(asin.group(1))
import regex as re
import json

def is_asin(text):
    # ASINs are typically 10-character alphanumeric strings..nice
    return bool(re.fullmatch(r'[A-Z0-9]{10}', text, flags=re.IGNORECASE))

def urlcleaner(input_file):
    result = []
    json_object = json.load(input_file)
    for line in json_object:
        url = line.get("url")
        #culling the URL
        asin_match = re.search(r'/[dg]p/([^/?]+)', url, flags=re.IGNORECASE)
        if asin_match:
            asin = asin_match.group(1)
            # check is it a valid ASIN
            if is_asin(asin):
                result.append(asin)
    return result

# Testing function
# def test_urlcleaner():
#     print("Testing begin")
#     test_target = open('sample.json', 'r')
#     result = urlcleaner(test_target)
#     print("Final Result:", result)

#     return result