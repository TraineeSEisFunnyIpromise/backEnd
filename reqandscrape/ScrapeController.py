
from flask import Flask, Blueprint, request, jsonify, session
from Reqandscrape.requestsender.chatgptreqsender import receiveinput,receiveinputtest
from Reqandscrape.zeroshotclassify import calculate_the_zeroshot
from Reqandscrape.search_scrape.PWBDscraperAZ import scrape_amazon
from Reqandscrape.NDcalculate import normal_dist
#time stuff
#nested asyncio nice
import nest_asyncio,pandas
# asyncio and werkzeug
# from werkzeug.wrappers import Request, Response
# from werkzeug.middleware.proxy_fix import ProxyFix
import csv
#
from flask_cors import CORS
import json
# instantiate the app

#JWT import
# Configure secret key for session signing (important for security)


search_bp = Blueprint('search', __name__)
nest_asyncio.apply()
#----------------------------------- Custom Middleware -----------------------------------
# def cors_middleware(app):
#     @Request.application
#     def middleware(request):
#         if request.method == "OPTIONS":
#             return Response("", status=204, headers={
#                 "Access-Control-Allow-Origin": "*",
#                 "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
#                 "Access-Control-Allow-Headers": "Content-Type, Authorization"
#             })

#         # Forward the request to the Flask app
#         response = app.full_dispatch_request()

#         # Modify the response headers to include CORS headers
#         response.headers["Access-Control-Allow-Origin"] = "*"
#         response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
#         response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
#         return response

#     return middleware

## Apply the custom middleware
# app.wsgi_app = ProxyFix(cors_middleware(app))
#-------------------------------------import and setup stuff ---------------------------------------

#--------------------------------------------search Prod sender Part--------------------------------------------

@search_bp.route('/scrape', methods=['POST'])
def scrape():	
    response = request.get_json()  # Store the JSON body request
    inputsearch = response[0]
    inputpeople = response[1]
    #(inputsearch,inputpeople)
    print("======doing task=====")
    result = scrape_amazon(inputsearch,inputpeople)
    print("\t ======sending result=====")
    print(type(result))
    print(result)

    return jsonify(result)

#--------------------------------------------search criteria sender Part--------------------------------------------
@search_bp.route('/search_criteria', methods=['POST'])
def search_criteria_sender():
	response = request.get_json() # store the json body request
	inputsearch = response[1] 
	inputpeople = response[0]
	print(inputpeople,inputsearch)
	response = receiveinput(inputsearch,inputpeople)
	with open("request_criteria.txt", "w+",encoding="utf-8") as f:
		print("enter loop raw result")
		if(response is not None):
			f.write(response)	
	print("======yeeting data=====")

	if isinstance(type(response),str):
		response = json.loads(response)
		return  response
	else:
		response = None
		return jsonify(response)

#--------------------------------------------search criteria sender Part--------------------------------------------


@search_bp.route('/critandprod', methods=['POST'])
def zeroshotstuff():

	response = request.get_json() # store the json body request
	inputdata = response[1] 
	inputcriteria = response[0]
	# print("input data : " + str(inputdata))
	# print("input criteria : "+ str(inputcriteria))
	result = calculate_the_zeroshot(inputdata,inputcriteria)
	result = json.dumps(result, indent=4)
	print("critandprod result " + str(result))
	if session==True:
		print("save data")
	return jsonify(result)

@search_bp.route('/nd', methods=['POST'])
def normaldistribution():
	result = normal_dist()
	print(result)
	if session==True:
		print("save data")
	return jsonify(result)

#in case when not using scrape
# #--------------------------------------------search test Part--------------------------------------------
@search_bp.route('/search_criteria_test', methods=['POST'])
def search_criteria_test_sender():
	response = request.get_json() # store the json body request
	print(response)
	a = receiveinputtest()
	print(response)
	return jsonify(a)

@search_bp.route('/scrape_test', methods=['POST'])
def scrape_test():
    response = request.get_json()  # Store the JSON body request
    print(response)

    try:
        with open('sample.json', 'r', encoding='utf-8') as f:
            results = json.load(f)
    except FileNotFoundError:
        return jsonify({"error": "File not found."}), 404
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Invalid JSON data: {e}"}), 400

    # Process scraped results (e.g., convert to JSON, store in database)
    return jsonify(results)


# @search_bp.route('/critandprod_test', methods=['POST'])
# def zeroshotstuff_test():

# 	result = [{'Label': 'Politics', 'Score': 0.07649134406967768}, {'Label': 'Automobile', 'Score': 0.32627149304700276}, {'Label': 'Sports', 'Score': 0.12833939120173454}, {'Label': 'Business', 'Score': 0.2105391121927708}, {'Label': 'World', 'Score': 0.25835864565202166}]
# 	result = json.dumps(result, indent=4)
# 	if session==True:
# 		print("save data")
# 	return jsonify(result)

# @search_bp.route('/nd_test', methods=['POST'])
# def normaldistribution_test():

# 	result = [33, 88, 55, 267]
# 	if session==True:
# 		print("save data")
# 	return jsonify({'data':result})




# Load the JSON data
#test section



# when want to use it independently
# search_term = input("Please type some input: ")
# # from reqandscrape.requestsender.chatgptreqsender import receiveinput
# search_term = "binocular"
# search_group = ""
# asyncio.run(scrape_amazon(search_term,search_group))
# asyncio.run(scrape_amazon_product(asin=["B095X25X25"]))