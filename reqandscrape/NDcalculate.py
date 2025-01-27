import numpy as np
import json

def normal_dist():
    #literally copy from somewhere which what it will be use here is like
    #x is number of size
    #sd standard deviation which used numpy lib formula is 
    #mean use numpy lib but formula is (total)/size
    sending_result = None
    x=None
    sd = None
    mean=None
    normal_distribution = None

    with open('sample.json', 'r', encoding='utf-8') as json_file:
            content = json_file.read()
            print("before check content")
            if content:
                print("The JSON file is loading")
                parsed_json = json.loads(content)

                if isinstance(parsed_json, list) and len(parsed_json) > 0:
                    first_item = parsed_json[0]
                    if isinstance(first_item, dict):
                        print("Column headers:", list(first_item.keys()))
                    else:
                        print("The first item in the JSON data is not a dictionary")
                else:
                    print("The JSON data is not a list or is empty")

                
                prices = [int(float(item['price'].replace('$', '').replace(',', ''))) 
          for item in parsed_json 
          if 'price' in item and item['price'] is not None 
          and item['price'].strip() != 'None'] 
                print("Prices:", prices)





                x = len(prices)
                print("size "+str(x))
                sd = np.std(prices)
                print("standard deviation "+str(sd))
                mean = np.mean(prices)
                print(mean)
                normal_distribution = (np.pi * sd) * np.exp(-0.5 * ((x - mean) / sd) ** 2)
                print(normal_distribution)
                sending_result = [int(x), int(sd), int(mean), int(normal_distribution)]
            else:
                print("The JSON file is empty")

    print("sending result = "+ str(sending_result))
    return sending_result