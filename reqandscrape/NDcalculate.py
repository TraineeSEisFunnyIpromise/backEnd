import numpy as np
import json

def normal_dist():
    #literally copy from somewhere which what it will be use here is like
    #x is number of size
    #sd standard deviation which used numpy lib formula is 
    #mean use numpy lib but formula is (total)/size
    with open('temporary_search_result.json', 'r', encoding='utf-8') as json_file:
      result = json.dump(json_file, ensure_ascii=False, indent=4)
    x = len(result)
    sd = np.std(result['price'])
    mean = np.mean(result['price'])
    normal_distribution = (np.pi*sd) * np.exp(-0.5*((x-mean)/sd)**2)
    sending_result = [x,sd,mean,normal_distribution]
    return sending_result

