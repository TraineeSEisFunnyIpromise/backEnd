
from flask import Flask, Blueprint, request, jsonify, session
from pymongo import MongoClient
from reqandscrape.chatgptreqsender import receiveinput
from reqandscrape.search_scrape.PWBDscraperAZ import save_scrape_test_data
from reqandscrape.scrape.PWRAZscrape import search_review
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

#-------------------------------------import and setpu stuff ---------------------------------------



#--------------------------------------------criteria sender Part--------------------------------------------

@search_bp.route('/compare_test', methods=['POST'])
def search_criteria():
	response = request.get_json() # store the json body request
	inputa = response['search_input']
	response = receiveinput(inputa)
	return response


#--------------------------------------------search Prod sender Part--------------------------------------------
@search_bp.route('/search_prod', methods=['POST'])
def search_prod():
	response = request.get_json() # store the json body request
	inputa = response['search_refined']
	response = search_prod(inputa)
	return response

#--------------------------------------------search Review sender Part--------------------------------------------@search_bp.route('/search_prod', methods=['POST'])
@search_bp.route('/search_review', methods=['POST'])
def search_review():
	response = request.get_json() # store the json body request
	inputa = response['search_refined']
	response = search_review(inputa)
	return response