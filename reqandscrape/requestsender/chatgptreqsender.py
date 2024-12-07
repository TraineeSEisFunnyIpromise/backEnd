
sentence = """Capacity: Do you usually toast for one or two people? Standard toasters have 2 slices, but wider models can handle 4.
Slot size: Consider what types of bread you toast. If you like bagels or thick Texas toast, wider slots are a must. Long slots are handy for long slices of bread.
Browning controls: How precise do you want your toast? Some toasters have a simple dial, while others offer many shade settings for perfectly customized browning.
Features: Do you want a defrost function for frozen bread? A reheat setting for keeping toast warm? Bagel setting that toasts the inside but barely touches the outside? Consider which features would be most useful to you.
Ease of cleaning: Look for a toaster with a removable crumb tray for easy cleaning.
Budget: Toasters range in price from basic models to high-end ones with lots of features. Decide how much you're comfortable spending.
Style: While not the most important factor, some toasters come in a variety of styles to match your kitchen décor."""


from openai import OpenAI
import re
import requests
import json
import os

openai_api_key = ""
openai_api_key2 = ""

def change_data(input, group_target):
    if openai_api_key is None:
        raise ValueError("OpenAI API key is not set in environment variables.")

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": f"Could you provide a criteria list according to the product with number? The product: {input} and for this group of people: group target: {group_target}"
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        # Process successful response
        criteria_list = response.json()['choices'][0]['message']['content']
        print("Response from OpenAI:", response.json())
        print("Criteria", criteria_list)
        print("------------------------------------------")
        print('\n')
        return criteria_list

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        print("Failed to retrieve criteria list.")
        return None  # Or return a specific error message/object

    except KeyError as e:
        print(f"Error: Missing key in response: {e}")
        print("Failed to parse response.")
        return None  # Or return a specific error message/object


#check word by chatGPT 55555555555555+
def check_input_word(input,group_target):
	if openai_api_key is None:
		raise ValueError("OpenAI API key is not set in environment variables.")

	url = "https://api.openai.com/v1/chat/completions"

	headers = {
	"Content-Type": "application/json",
	"Authorization": f"Bearer {openai_api_key2}"
	}
	data = {
	"model": "gpt-4o-mini",
		"messages": [
			{
			"role": "system",
			"content": "You are a helpful assistant."
			},
			{
			"role": "user",
			"content": """could you check that input product 
			is it related to electric device or not and determine an input
			is relevant to any of these categories: 
			"1. Occupation: e.g., teacher, engineer, nurse, student\n"
      "2. Age Group: e.g., child, teenager, young adult, adult, senior\n"
      "3. Wealth Status: e.g., low income, middle income, high income\n\n".
			please answer in true or false only : """ + "group target : " + group_target + "product target : "+ input
			}
		]
	}

	try:
			response = requests.post(url, headers=headers, json=data)
			response.raise_for_status()  # Raise an exception for non-200 status codes

			# Process successful response
			criteria_list = response.json()['choices'][0]['message']['content']
			print("Response from OpenAI:", response.json())
			print("result check:", criteria_list)
			print("------------------------------------------")
			print('\n')
			return criteria_list

	except requests.exceptions.RequestException as e:
			print(f"Error: {e}")
			print("Failed to retrieve result.")
			return None  # Or return a specific error message/object

	except KeyError as e:
			print(f"Error: Missing key in response: {e}")
			print("Failed to parse response.")
			return None  # Or return a specific error message/object



def extract_criteria(text):
    # Split the text by lines
	if text != None:
		lines = text.strip().split('\n')
		
		# Initialize arrays to store headings and details
		headings = []

		for line in lines:
			# Split the line at the first ":"
			parts = line.split(":", 1)
			if len(parts) == 2:
				heading = parts[0].strip()
				headings.append(heading)
		return headings
	else:
		return None

def pick_numbered_headlines(input_list):
    # Initialize an empty list to store the filtered headlines
    numbered_headlines = []

    # Iterate through each item in the input list
    for item in input_list:
        # Check if the item starts with a number followed by a period
        if item.strip().split('.')[0].isdigit():
            # If it matches the condition, add it to the list of numbered headlines
            numbered_headlines.append(item.strip())

    return numbered_headlines

#what will use
def receiveinput(input_text,group_target):
	storea = []
	counta = 0
	print("---------------------raw input----------------------")
	print(input_text)
	#check word 
	if str.lower(check_input_word(input_text,group_target)) == "true":
		print("---------------------setup input----------------------")
		#what is goin on here is search -> extract criteria -> remove any headline that aren't 
		#number included
		set_text = pick_numbered_headlines(extract_criteria(change_data(input_text,group_target)))
		print(set_text)
		print("----------------------------------------------------")

		for i in range(len(set_text)):
				storea.append((set_text[i]))

		lenj = len(storea) +1

		for i in range(len(storea)):
				for j in range(lenj):
						if storea[i] == None:
								a = storea[j-1]
								storea[j-1] = storea[i]
								storea[i] = a
		#remove None Value
		for i in range(len(storea)):
				if storea[i] == None:
						counta += 1
		for i in range(counta):
				storea.pop(0)
		pick_numbered_headlines(storea)


		print("------")
		print(storea)
		return storea
	else:
		return "Invalid"

#run test
def receiveinputtest():
   set_text = extract_criteria(sentence)
   storea = []
   counta = 0
   for i in range(len(set_text)):
      storea.append((set_text[i]))
   lenj = len(storea) +1

   for i in range(len(storea)):
      for j in range(lenj):
          if storea[i] == None:
              a = storea[j-1]
              storea[j-1] = storea[i]
              storea[i] = a

   for i in range(len(storea)):
       if storea[i] == None:
           counta += 1
   for i in range(counta):
       storea.pop(0)
   print("------")
   print(storea)

   return storea
