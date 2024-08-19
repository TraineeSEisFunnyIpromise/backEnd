import transformers  
from pymongo import MongoClient
#-------------------------import library Above-----------------------------

client = MongoClient('mongodb://localhost:27017')
db = client['Database1']
usercollection = db['DB1']
#-------------------------set up mongoDB for testing Above-----------------------------


classifier = transformers.pipeline("zero-shot-classification", model="facebook/bart-large-mnli")  
#sample text and label
text = "I enjoy playing cricket, specializing as a left-arm leg spinner while showcasing my skills as a right-handed one-down batsman." 
labels = ['Politics', 'Automobile', 'Sports', 'Business', 'World']  



def compare_prod(criteria_lists, inputa):
	prediction = classifier(inputa, criteria_lists)
	return prediction

def compare_test(criteria_lists, inputa):
	prediction = classifier(inputa, criteria_lists)  

	print(prediction['sequence']) 
	print(prediction['labels']) 
	print(prediction['scores'])