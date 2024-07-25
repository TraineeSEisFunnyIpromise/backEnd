
from flask import Flask, Blueprint, request, jsonify, session
from flask_session import Session
from flask_cors import CORS
from pymongo import MongoClient
from comparesys.comparefile.compare import search_pattern
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
# CORS(app, resources={r'/*': {'origins': '*'}})
#JWT import
# Configure secret key for session signing (important for security)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_PERMANENT'] = False  # Set to True for persistent sessions (browser closed)
app.config['SESSION_TYPE'] = 'filesystem'  # Or use a database or Redis for storage
app.config['PERMANENT_SESSION_LIFETIME'] = 300


auth_bp = Blueprint('auth', __name__)

#-------------------------------------import and setpu stuff ---------------------------------------



#--------------------------------------------Login Part--------------------------------------------

@auth_bp.route('/login', methods=['POST'])
def login():
	login_details = request.get_json() # store the json body request
	usernameA = login_details['username']
	passA = login_details['password']
# check if user exist
	user_from_db = usercollection.find_one({"username": login_details["username"]}) 
# man i hate how it look down here
	if user_from_db:
  #process to check mongodb server with boolean didn't know python could just pull that move
		if bool(is_mongodb_available()) != False:
			if (passA == user_from_db['password']):
							#SESSION with Flask is Funni
				session['username'] = usernameA  # Set username in session
    #return success
				return jsonify({'msg':'login successful'}),200
			else:
    #return login not suckcess
				return jsonify({'msg': 'The username or password is incorrect'}),200
		else:
    #return database bad
			return jsonify({'msg': 'The database is down!!!'}),504
	else:
    #return server is fxck
		return jsonify({'msg':'Server is not avaliable'}),400

#---------------------------------------- Session status-------------------------------------------
@auth_bp.route('/sessioncheck',methods=['POST'])
def something():
			username = session.get('user')
				# Calculate time left until session expires (server-side)
			session_start_time = session.get('start_time')
                  #time zone magic but seem deprecrated... dawg
			now = datetime.utcnow
			duration_left = session_start_time + timedelta(seconds=app.config['PERMANENT_SESSION_LIFETIME']) - now
			response = username + "  " + duration_left
			return response

#----------------------------------------register part--------------------------------------------

@auth_bp.route('/register', methods=['POST'])
def register():
    new_user = request.get_json() # store the json body request
    #below code literally check for juse username but who will check different password? aren't that leak already?
		# bro who on earth check password of the similar name person? and if so isn't that we leak the info of account
		# that have the same name???
    doc = usercollection.find_one({"username": new_user["username"]}) # check if user exist like
    #after checking logic
    if not doc:#pass
        usercollection.insert_one(new_user)
        return jsonify({'msg': 'User created successfully'}), 201
		
    else:#error given
        return jsonify({'msg': 'Username already exists'}), 409


#---------------------------------- pure function around here--------------------------------
#check all data
def check_database():
  # Find all documents in the collection
  documents = list(usercollection.find())
  # Check if any documents were found
  if documents:
    message = "Database contains documents!"
    return jsonify({'message': message})
  else:
    message = "Database is empty."
    data = None
  return jsonify({'message': message})

def is_mongodb_available():
  result = False
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
