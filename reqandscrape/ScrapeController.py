
from flask import Flask, Blueprint, request, jsonify, session
from pymongo import MongoClient
from Reqandscrape.requestsender.chatgptreqsender import receiveinput,receiveinputtest
from Reqandscrape.zeroshotclassify import calculate_the_zeroshot,calculate_the_zeroshot_test
#time stuff
#nested asyncio nice
import nest_asyncio,pandas
# asyncio and werkzeug
from werkzeug.wrappers import Request, Response
from werkzeug.middleware.proxy_fix import ProxyFix
import asyncio,csv
#
from flask_cors import CORS
from datetime import datetime, timedelta
import json
# instantiate the app
app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017')
db = client['Database1']
usercollection = db['DB1']
# enable CORS
cors = CORS(app, resources={r"/*": {"origins": "*"}})
#JWT import
# Configure secret key for session signing (important for security)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_PERMANENT'] = False  # Set to True for persistent sessions (browser closed)
app.config['SESSION_TYPE'] = 'filesystem'  # Or use a database or Redis for storage
app.config['PERMANENT_SESSION_LIFETIME'] = 300

search_bp = Blueprint('search', __name__)
nest_asyncio.apply()
#----------------------------------- Custom Middleware -----------------------------------
def cors_middleware(app):
    @Request.application
    def middleware(request):
        if request.method == "OPTIONS":
            return Response("", status=204, headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization"
            })

        # Forward the request to the Flask app
        response = app.full_dispatch_request()

        # Modify the response headers to include CORS headers
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

    return middleware

# Apply the custom middleware
app.wsgi_app = ProxyFix(cors_middleware(app))
#-------------------------------------import and setup stuff ---------------------------------------

#--------------------------------------------search Prod sender Part--------------------------------------------

@search_bp.route('/scrape', methods=['POST'])
def scrape():
    response = request.get_json()  # Store the JSON body request
    inputsearch = response[0]
    inputpeople = response[1]
    #(inputsearch,inputpeople)
    print("======doing task=====")
    # scrape_amazon(inputsearch,inputpeople)
    result = csv_to_json("search_result_recent.csv","search_result_dumb.json")
    print("======sending result=====")
    print(type(result))

    return jsonify(result)

#--------------------------------------------search criteria sender Part--------------------------------------------
@search_bp.route('/search_criteria', methods=['POST'])
def search_criteria_sender():
	response = request.get_json() # store the json body request
	inputsearch = response[1] 
	inputpeople = response[0]
	print(inputpeople,inputsearch)
	response = receiveinput(inputsearch,inputpeople)
	print("======yeeting data=====")
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
	if session==True:
		target_user = usercollection.find(session['username'])
		usercollection[target_user].insert({"zeroshoted":result})
	return jsonify(result)

#--------------------------------------------search test  Part--------------------------------------------
@search_bp.route('/search_criteria_test', methods=['POST'])
def search_criteria_test_sender():
	response = request.get_json() # store the json body request
	print(response)
	a = receiveinputtest()
	print(response)
	return jsonify(a)

@search_bp.route('/search_prod_test', methods=['POST'])
def search_prod_sender_test():
	response = request.get_json() # store the json body request
	print(response)
	with open('Reqandscrape\search_scrape\search_result_recent.csv', mode ='r')as file:
		csvFile = csv.reader(file)
		result = csvFile
	response = result
	return jsonify(response)

@search_bp.route('/scrape_test', methods=['POST'])
async def scrape_test():
	response = request.get_json() # store the json body request
	print(response)
	results = json_data_mock()
	# Process scraped results (e.g., convert to JSON, store in database)
	return jsonify(results)

@search_bp.route('/critandprod_test', methods=['POST'])
def zeroshotstuff_test():
	response = request.get_json() # store the json body request
	print(response)
	result = calculate_the_zeroshot_test()
	print(result)
	return jsonify(result)

# Load the JSON data
#test section


#dumb solution 


# when want to use it independently
# search_term = input("Please type some input: ")
# # from reqandscrape.requestsender.chatgptreqsender import receiveinput
# search_term = "binocular"
# search_group = ""
# asyncio.run(scrape_amazon(search_term,search_group))
# asyncio.run(scrape_amazon_product(asin=["B095X25X25"]))