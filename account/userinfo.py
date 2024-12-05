# app.py
from flask import Flask, jsonify, session
from flask_cors import CORS
from database.databasemanager import update_user_aboutme,check_database_status,access_database,delete_user,update_password
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

def update_aboutme(data):
  username = session.get('user')
  if data["send" != '']:
    if check_database_status() == True:
      update_user_aboutme(data,username)
    else:
      return
    return jsonify({'message': 'Registration successful'})
  else:
    return jsonify({'error': 'Please provide username and password'})


def update_oldpassword(username,get_resetpassword):
  if get_resetpassword != '':
        update_password(username,get_resetpassword)
  else:
    return jsonify({'error': 'Please providepassword'})
  return jsonify({'message': 'Reset password successful'})


def userinfo():
	    # Check if the user is logged in by verifying the session
    if 'username' in session:
        username = session['username']
        
        # Find the user in the database using the username from the session
        if check_database_status == True:
          user = access_database(username)
        if user == True:
            # Return user data (excluding sensitive information)
            return jsonify({'username': user['username'], 'about me': user.get('about me', 'No information available')}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    else:
        # User is not logged in or session has expired
        return jsonify({'error': 'Unauthorized'}), 401


def delete_account(username,password):
	user_from_db = access_database(username)
	if password == user_from_db['password']:
		delete_user(username)
		return jsonify({'msg' : 'remove succesful' }), 200
	else:
		return jsonify({'msg': 'incorrect password'}), 400
	




if __name__ == '__main__':
    app.run()
