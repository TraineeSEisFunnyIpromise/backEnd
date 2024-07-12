# app.py
from flask import Flask, Blueprint, request, jsonify, session
from flask_session import Session
from flask_cors import CORS
from pymongo import MongoClient
from comparesys.compare import search_pattern
from reqandscrape.chatgptreqsender import receiveinput
from functools import wraps
#time stuff
from datetime import datetime, timedelta
# instantiate the app
app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017')
db = client['Database1']
usercollection = db['DB1']
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

#for real thou no need to initialize the session it up in main...why i keep doing this?
# Initialize Flask-Session
Session(app)

auth_bp = Blueprint('userinfo', __name__)
#-------------------------------------import and setpu stuff ---------------------------------------


#                                        Session status
@auth_bp.route('/sessioncheck',methods=['POST'])
def something():
			username = session.get('user')
				# Calculate time left until session expires (server-side)
			session_start_time = session.get('start_time')
			now = datetime.utcnow
			duration_left = session_start_time + timedelta(seconds=app.config['PERMANENT_SESSION_LIFETIME']) - now
			response = username + "  " + duration_left
			return response


#----------------------------------------User info part--------------------------------------------
@auth_bp.route('/update', methods=['POST'])
def update():
		data = request.json
		collection = db['DB1']
		result = collection.insert_one(data)
		user_id = data.get('user_id')
		name = data.get('name')
		email = data.get('email')
		if result.acknowledged:
				data = {
        "userinfo"         : data.get('userinfo')
        }
				collection.insert_one(data)
				return jsonify({'message': 'Registration successful'})
		else:
				return jsonify({'error': 'Please provide username and password'})
    
#view data seem it use dump? 


@auth_bp.route('/userinfo', methods=['POST'])
def profile():
	username = session['username']
	user_from_db = usercollection.find_one({'username' : username})
	if user_from_db:
		del user_from_db['_id'], user_from_db['password'] # delete data we don't want to return
		return jsonify({'profile' : user_from_db }), 200
	else:
		return jsonify({'msg': 'Profile not found'}), 404
     

# @app.route('/search', methods=['POST'])
# def search_products():
#     if request.method == 'POST':
#         #send data back to request which '/search'
#         search_keyword = request.get_json()
#         searchword = search_keyword['keyword']
#         result = receiveinput(searchword)
#         return jsonify({'msg':result})
#     else :
#         return 'methods not allowed', 405


#start app down here _main_


if __name__ == '__main__':
    app.run()
