# app.py
from flask import Flask, Blueprint, request, jsonify, session
from flask_cors import CORS
from pymongo import MongoClient
from account.Authentication import yeetusername
from database.databasemanager import update_user,check_database_status,access_database,delete_user

from functools import wraps
#time stuff
from datetime import datetime, timedelta
# instantiate the app
app = Flask(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

#for real thou no need to initialize the session it up in main...why i keep doing this?
# Initialize Flask-Session
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_PERMANENT'] = False  # Set to True for persistent sessions (browser closed)
app.config['SESSION_TYPE'] = 'filesystem'  # Or use a database or Redis for storage
app.config['PERMANENT_SESSION_LIFETIME'] = 300

#-------------------------------------import and setpu stuff ---------------------------------------

#                                        Session status

def sessioncheck():
			username = session.get('user')
				# Calculate time left until session expires (server-side)
			session_start_time = session.get('start_time')
			now = datetime.utcnow
			duration_left = session_start_time + timedelta(seconds=app.config['PERMANENT_SESSION_LIFETIME']) - now
			response = username + "  " + duration_left
			return jsonify(response)

#----------------------------------------User info part--------------------------------------------

def update():
  data = request.json
  username = session.get('user')
  if data["send" != '']:
    if check_database_status() == True:
      update_user(data,username)
    else:
      return
    return jsonify({'message': 'Registration successful'})
  else:
    return jsonify({'error': 'Please provide username and password'})


def userinfo():
	    # Check if the user is logged in by verifying the session
    if 'username' in session:
        username = session['username']
        
        # Find the user in the database using the username from the session
        if check_database_status == True:
          user = access_database(username)
        
        if user == True:
            # Return user data (excluding sensitive information)
            return jsonify({'username': user['username'], 'about': user.get('about', 'No information available')}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    else:
        # User is not logged in or session has expired
        return jsonify({'error': 'Unauthorized'}), 401
	
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

def Delete():
	data = request.json
	username = data['username']
	passA = data['password']
	user_from_db = access_database(username)
	if passA == user_from_db['password']:
		delete_user(username)
		return jsonify({'msg' : 'remove succesful' }), 200
	else:
		return jsonify({'msg': 'Profile not found'}), 404
	


#methods
def check_username():
	return

def get_user():
	return

def update_to_database():
	return

def remove_user():
	return
#start app down here _main_


if __name__ == '__main__':
    app.run()
