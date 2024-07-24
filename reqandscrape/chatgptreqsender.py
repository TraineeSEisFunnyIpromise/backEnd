from openai import OpenAI
import re
import requests
import json
import os



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

def change_data(input):
	if openai_api_key is None:
		raise ValueError("OpenAI API key is not set in environment variables.")

	url = "https://api.openai.com/v1/chat/completions"

	headers = {
	"Content-Type": "application/json",
	"Authorization": f"Bearer {openai_api_key}"
	}
	data = {
	"model": "gpt-3.5-turbo",
	"messages": [
		{
		"role": "system",
		"content": "You are a helpful assistant."
		},
		{
		"role": "user",
		"content": "could you become an expert according to this input?"+input+"and after that give me a critiria limit 5 critiria"
		}
	]
	}
	response = requests.post(url, headers=headers, json=data)
	# Check if the request was successful
	if response.status_code == 200:
		print("Response from OpenAI:", response.json())
		print("------------------------------------------")
		print('\n')
		print(response.json()['choices'][0]['message']['content'])
	else:
		print("Error:", response.status_code, response.text)
	return response.json()['choices'][0]['message']['content']

def select_headline(text):
  match = re.search(r"(.*):\s+(\w+)", text)  # Matches text followed by ":" and a word
  if match:
    return match.group(1) + ":"  # Captures group 1 (text before ":") and adds ":"
  else:
    return None  # Return None if no match


def segment_text(text):
  segments = re.split(r"\.", text)  # Split at "."
  return segments

def segment_semi(text):
   storea = []
   for i in range(len(text)):
      storea.append(select_headline(text[i]))
   print(storea)
   print("------")
   return storea

def cutthatnull(text):
   storea = []
   for i in range(len(text)):
      storea.append(select_headline(text[i]))
   print(storea)
   print("------")
   return storea

#what will use
def receiveinput(text):
   set_text = segment_text(change_data(text))
   storea = []
   for i in range(len(set_text)):
      storea.append(select_headline(set_text[i]))
   print(storea)
   print("------")
   return storea

#run test
def receiveinputtest(text):
   set_text = segment_text(text)
   storea = []
   for i in range(len(set_text)):
      storea.append(select_headline(set_text[i]))
   print(storea)
   print("------")
   return storea
#test
# receiveinput(input("type here :"))
# receiveinputtest(sentence)