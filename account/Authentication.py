
from flask import Flask, Blueprint, request, jsonify, session
from flask_session import Session
from flask_cors import CORS
from database.databasemanager import check_username,access_database,add_new_user,check_database_status
from functools import wraps
#time stuff
from datetime import datetime, timedelta
import uuid
# instantiate the app
app = Flask(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
#JWT import
# Configure secret key for session signing (important for security)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_PERMANENT'] = False  # Set to True for persistent sessions (browser closed)
app.config['SESSION_TYPE'] = 'filesystem'  # Or use a database or Redis for storage
app.config['PERMANENT_SESSION_LIFETIME'] = 300


#-------------------------------------import and setpu stuff ---------------------------------------



#--------------------------------------------Login Part-------------------------------------------

def login(self, username, password):
	#check database status
      if check_database_status != False :
          #access account data according to name
          if check_username(username) != None or check_username(username) != '':
            user_from_db = access_database(username)
            if user_from_db != None or user_from_db != '':
              result = user_from_db
              return result
      else:
            return jsonify({'msg': 'The database is down!!!'}),504


def logout():
    session.clear()
#---------------------------------------- Session status-------------------------------------------

def something():
			username = session.get('user')
				# Calculate time left until session expires (server-side)
			session_start_time = session.get('start_time')
                  #time zone magic but seem deprecrated... dawg
			now = datetime.utcnow
			duration_left = session_start_time + timedelta(seconds=app.config['PERMANENT_SESSION_LIFETIME']) - now
			response = username + "  " + duration_left
			return jsonify(response)

#----------------------------------------register part--------------------------------------------

def register():
    new_user = request.get_json() # store the json body request
    user_id = str(uuid.uuid4())
    #find user
    doc = check_username(new_user["username"]) # check if user exist like
    #after checking no same username detected
    if not doc:#pass
        new_user['user_id'] = user_id
        add_new_user(new_user)
        return jsonify({'msg': 'User created successfully'}), 201
		
    else:#error given
        return jsonify({'msg': 'Username already exists'}), 409


#-------------------------------------------------------------------------------------
#-----------------------------end of Login & Registration-------------------------------------
Session(app)

if __name__ == '__main__':
    app.run()
