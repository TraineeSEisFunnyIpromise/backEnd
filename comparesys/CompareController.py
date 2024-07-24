
from flask import Flask, Blueprint, request, jsonify, session
from pymongo import MongoClient
from reqandscrape.search_scrape.PWBDscraperAZ import save_scrape_test_data
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


compare_bp = Blueprint('compare', __name__)

#-------------------------------------import and setpu stuff ---------------------------------------

#--------------------------------------------search Prod sender Part--------------------------------------------
@compare_bp.route('/compare', methods=['POST'])
def compare_prod():
	response = request.get_json() # store the json body request
	inputa = response['search_refined']
	response = compare_prod(inputa)
	return response

#--------------------------------------------compare test sender Part--------------------------------------------@search_bp.route('/search_prod', methods=['POST'])
@compare_bp.route('/compare_test', methods=['POST'])
def compare_test():
	response = request.get_json() # store the json body request
	inputa = response['search_refined']
	response = save_scrape_test_data()
	print(inputa)
	return response