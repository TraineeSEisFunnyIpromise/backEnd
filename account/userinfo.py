# app.py
from flask import Flask, Blueprint, request, jsonify, session
from flask_cors import CORS
from pymongo import MongoClient
from account.Authentication import yeetusername

from functools import wraps
#time stuff
from datetime import datetime, timedelta
# instantiate the app
app = Flask(__name__)

client = MongoClient('mongodb://localhost:6000')
db = client['Database2']
usercollection = db['db1']
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
		user = yeetusername
		collection = db['DB1']
		if data["send" != '']:
				data = {
        "userinfo"         : data.get('userinfo')
        }
				collection.insert_one(data)
				return jsonify({'message': 'Registration successful'})
		else:
				return jsonify({'error': 'Please provide username and password'})

@userinformation_bp.route('/Information', methods=['POST'])
def userinfo():
	    # Check if the user is logged in by verifying the session
    if 'username' in session:
        username = session['username']
        
        # Find the user in the database using the username from the session
        user = usercollection.find_one({"username": username})
        
        if user:
            # Return user data (excluding sensitive information)
            return jsonify({'username': user['username'], 'about': user.get('about', 'No information available')}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    else:
        # User is not logged in or session has expired
        return jsonify({'error': 'Unauthorized'}), 401
	# # user_id = usercollection.find_one({"user_id": encrypted_username}) 
	# user = usercollection.find_one(yeetusername())  
	# print(user)
	# if user:
	# 	 #this should be session check ut meh
	# 	if user:
	# 	# Return user data (excluding sensitive information)
	# 		return jsonify({'username': user['username'], 'about': user['about']})  # Example
	# 	else:
	# 		return jsonify({'error': 'User not found'}), 404
	# else:
	# 	return jsonify({'error': 'Unauthorized'}), 401

@userinformation_bp.route('/Information_test', methods=['POST'])
def userinfo_test():
	# user_id = usercollection.find_one({"user_id": encrypted_username}) 
	user = {  "username": "admin",
					"password:":"1234",
            "about":"something",
            "question_r":"do you like banana",
            "answer_r":"Yes",
            "roles": "Administrator",} 
	print(user)
	if user:
		 #this should be session check ut meh
		if user:
		# Return user data (excluding sensitive information)
			return jsonify({'username': user['username'], 'about': user['about']})  # Example
		else:
			return jsonify({'error': 'User not found'}), 404
	else:
		return jsonify({'error': 'Unauthorized'}), 401

     
@userinformation_bp.route('/Delete', methods=['POST'])
def Delete():
	data = request.json
	username = data['username']
	passA = data['password']
	user_from_db = usercollection.find_one({'username' : username})
	if passA == user_from_db['password']:
		usercollection.remove(username)
		return jsonify({'msg' : 'remove succesful' }), 200
	else:
		return jsonify({'msg': 'Profile not found'}), 404
	

#start app down here _main_


if __name__ == '__main__':
    app.run()
