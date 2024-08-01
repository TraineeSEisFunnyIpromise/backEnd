# app.py
from flask import Flask, Blueprint, request, jsonify, session
from flask_cors import CORS
from pymongo import MongoClient
from reqandscrape.requestsender.chatgptreqsender import receiveinput
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
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_PERMANENT'] = False  # Set to True for persistent sessions (browser closed)
app.config['SESSION_TYPE'] = 'filesystem'  # Or use a database or Redis for storage
app.config['PERMANENT_SESSION_LIFETIME'] = 300

userinformation_bp = Blueprint('userinfo', __name__)
#-------------------------------------import and setpu stuff ---------------------------------------

#                                        Session status
@userinformation_bp.route('/Sessioncheck',methods=['POST'])
def sessioncheck():
			username = session.get('user')
				# Calculate time left until session expires (server-side)
			session_start_time = session.get('start_time')
			now = datetime.utcnow
			duration_left = session_start_time + timedelta(seconds=app.config['PERMANENT_SESSION_LIFETIME']) - now
			response = username + "  " + duration_left
			return response

#----------------------------------------User info part--------------------------------------------
@userinformation_bp.route('/Update', methods=['POST'])
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

@userinformation_bp.route('/Information', methods=['POST'])
def userinfo():
    session_id = session.get('session_id')
    # Retrieve user data based on session_id (replace with your logic)
    user_data = {'username': 'John Doe', 'email': 'johndoe@example.com'}  # Example data
    return jsonify(user_data)
	# if user_from_db:
	# 	del user_from_db['_id'], user_from_db['password'] # delete data we don't want to return
	# 	return jsonify({'profile' : user_from_db }), 200
	# else:
	# 	return jsonify({'msg': 'Profile not found'}), 404
     
@userinformation_bp.route('/Delete', methods=['POST'])
def Delete():
	username = session['username']
	user_from_db = usercollection.find_one({'username' : username})
	if user_from_db:
		usercollection.remove(username)
		return jsonify({'profile' : user_from_db }), 200
	else:
		return jsonify({'msg': 'Profile not found'}), 404
	

#start app down here _main_


if __name__ == '__main__':
    app.run()
