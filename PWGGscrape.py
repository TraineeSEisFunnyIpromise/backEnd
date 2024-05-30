import requests
import csv

payload = {'api_key': 'APIKEY', 'q':'sushi' , 'gl':'us', 'num': '10'}
resp = requests.get('https://api.serpdog.io/search', params=payload)

data = resp.json()

with open('search_results.csv', 'w', newline='') as csvfile:
 csv_writer = csv.writer(csvfile)
 
 # Write the headers
 csv_writer.writerow(["Title", "Link", "Snippet"])
 
 # Write the data
 for result in data["organic_results"]:
  csv_writer.writerow([result["title"], result["link"], result["snippet"]])

  
print('Done writing to CSV file.')