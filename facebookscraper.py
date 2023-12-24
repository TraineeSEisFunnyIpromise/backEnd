import facebook
import os
# TOKEN = os.environ.get("ACCESS_TOKEN") # Your GraphAPI token here.
def main():
	
	TOKEN = ""
	graph = facebook.GraphAPI(TOKEN) 
	
	places = graph.search(type ='place', center ='28.6304, 77.2177',  
						fields ='name, location') 
	
	for place in places['data']: 
		print('%s %s' %(place['name'].encode(), place['location'].get('zip'))) 
      
if __name__ == '__main__': 
    main() 