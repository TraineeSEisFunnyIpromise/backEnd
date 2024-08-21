
from flask import Flask, Blueprint, request, jsonify, session
from pymongo import MongoClient
from Reqandscrape.Requestsender.chatgptreqsender import receiveinput,receiveinputtest
from Reqandscrape.Search_scrape.PWBDscraperAZ import scrape_amazon
from Reqandscrape.zeroshotclassify import calculate_the_zeroshot,calculate_the_zeroshot_test
#time stuff
from datetime import datetime, timedelta
# instantiate the app
app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017')
db = client['Database1']
usercollection = db['DB1']
# enable CORS
# CORS(app, resources={r'/*': {'origins': '*'}})
#JWT import
# Configure secret key for session signing (important for security)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_PERMANENT'] = False  # Set to True for persistent sessions (browser closed)
app.config['SESSION_TYPE'] = 'filesystem'  # Or use a database or Redis for storage
app.config['PERMANENT_SESSION_LIFETIME'] = 300


search_bp = Blueprint('search', __name__)

#-------------------------------------import and setup stuff ---------------------------------------

#--------------------------------------------search Prod sender Part--------------------------------------------
@search_bp.route('/search_prod', methods=['POST'])
def search_prod_sender():
	response = request.get_json() # store the json body request
	#format data
	print(response)
	inputsearch = response[1] 
	inputpeople = response[0]
	print(inputpeople,inputsearch)
	response = scrape_amazon(inputsearch,inputpeople)
	if session==True:
		target_user = usercollection.find(session['username'])
		usercollection[target_user].insert({"productdata":response})
	return jsonify(response)

#--------------------------------------------search criteria sender Part--------------------------------------------
@search_bp.route('/search_criteria', methods=['POST'])
def search_criteria_sender():

	response = request.get_json() # store the json body request
	inputsearch = response[1] 
	inputpeople = response[0]
	print(inputpeople,inputsearch)
	response = receiveinput(inputsearch,inputpeople)
	if session==True:
		target_user = usercollection.find(session['username'])
		usercollection[target_user].insert({"criteria":response})
	return jsonify(response)

#--------------------------------------------search criteria sender Part--------------------------------------------


@search_bp.route('/critandprod', methods=['POST'])
def zeroshotstuff():

	response = request.get_json() # store the json body request
	inputdata = response[1] 
	inputcriteria = response[0]
	result = calculate_the_zeroshot(inputdata,inputcriteria)
	# result = compare_prod(inputdata,inputcriteria)
	# if session==True:
	# 	target_user = usercollection.find(session['username'])
	# 	usercollection[target_user].insert({"zeroshoted":result})
	return jsonify(result)

#--------------------------------------------search test  Part--------------------------------------------
@search_bp.route('/search_criteria_test', methods=['POST'])
def search_criteria_test_sender():
	response = request.get_json() # store the json body request
	a = receiveinputtest()
	print(response)
	return jsonify(a)

@search_bp.route('/search_prod_test', methods=['POST'])
def search_prod_sender_test():
	response = request.get_json() # store the json body request
	inputa = response[0]
	response = open("resultscraper\_response_az_content.txt", 'r')
	return jsonify(response)

@search_bp.route('/critandprod_test', methods=['POST'])
def zeroshotstuff_test():
	result = calculate_the_zeroshot_test()
	print(result)
	return jsonify(result)