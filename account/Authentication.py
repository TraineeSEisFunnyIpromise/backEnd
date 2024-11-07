
from flask import Flask, Blueprint, request, jsonify, session
from flask_session import Session
from flask_cors import CORS
from database.databasemanager import check_username,access_database
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



#--------------------------------------------Login Part--------------------------------------------


def login():
	login_details = request.get_json() # store the json body request
	usernameA = login_details['username']
	passA = login_details['password']
	# print(login_details)
	user_from_db = 
# man i hate how it look down here
	if user_from_db:
  #process to check mongodb server with boolean didn't know python could just pull that move
		if bool(is_mongodb_available()) != False:
                  
			if (passA == user_from_db['password']):
				session['username'] = usernameA  # Store the username in the session
				print(f"Session after login: {session}")
				encrypted_username = usernameA
				user_from_db['user_id']= session  # Store user ID in session
				print(session)
				return jsonify({'message': 'login successful'}), 202
			else: #return login not suckcess
				return jsonify({'msg': 'The username or password is incorrect'}),401
		else: #return database bad
			return jsonify({'msg': 'The database is down!!!'}),504
	else: #return server is fxck
		return jsonify({'msg':'Server is not avaliable'}),400



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
    doc = usercollection.find_one({"username": new_user["username"]}) # check if user exist like
    #after checking no same username detected
    if not doc:#pass
        new_user['user_id'] = user_id
        usercollection.insert_one(new_user)
        return jsonify({'msg': 'User created successfully'}), 201
		
    else:#error given
        return jsonify({'msg': 'Username already exists'}), 409


def access_database(username):
  usertarget_data = usercollection.find_one({"username": username})
  return usertarget_data

#---------------------------------- pure function around here--------------------------------
#check all data

def authenticate(self, username, password):
	#check database status
      if is_mongodb_available != False :
          #access account data according to name
          if check_username(username) != None or check_username(username) != '':
            user_from_db = access_database(username)
            if user_from_db != None or user_from_db != '':
              result = user_from_db
              return result
      else:
            return jsonify({'msg': 'The database is down!!!'}),504
	

def check_username(username):
      user_from_db = access_database(username)
      if user_from_db != None or user_from_db != '':
        return True
      else:
        return False

def account_access(username):
  result = ''
  if is_mongodb_available != False :
    user_from_db = access_database(username)
    if user_from_db != None or user_from_db != '':
      result = user_from_db
      return result
  else:
      return None

def is_mongodb_available():
  try:
    # Attempt to connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    client.server_info()  # Perform a basic server info call
    message = "MongoDB is available!"
  except Exception as e:
    message = f"MongoDB connection error: {str(e)}"

  return jsonify({'message': message})
#-------------------------------------------------------------------------------------
#-----------------------------end of Login & Registration-------------------------------------
Session(app)

if __name__ == '__main__':
    app.run()
