# app.py
from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
from flask_cors import CORS
from pymongo import MongoClient
from compare import search_pattern
from chatgptreqsender import receiveinput
from functools import wraps

# instantiate the app
app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017')
db = client['Database1']
usercollection = db['DB1']
# enable CORS

CORS(app, resources={r'/*': {'origins': '*'}})
#JWT import
# Configure secret key for session signing (important for security)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_PERMANENT'] = False  # Set to True for persistent sessions (browser closed)
app.config['SESSION_TYPE'] = 'filesystem'  # Or use a database or Redis for storage
app.config['PERMANENT_SESSION_LIFETIME'] = 300
# Initialize Flask-Session
Session(app)

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        user_data = usercollection.find_one(username)  # Function to fetch user data from MongoDB
        if user_data:
            return 'user data found'
        else:
            return 'User data not found'
    else:
        return 'Please log in to view user information'

#Session * i should seperate this

# #Session status
# @app.route('',methods=[''])
# def something():
#     return 

#Login & Register Section
@app.route('/login', methods=['POST'])
def login():
	login_details = request.get_json() # store the json body request
	usernameA = login_details['username']
	passA = login_details['password']
	 # search for user in database
	user_from_db = usercollection.find_one({"username": login_details["username"]}) # check if user exist
	if user_from_db:
		if (passA == user_from_db['password']):
            #providing token with JWT ...they said it bad?
			session['username'] = usernameA  # Set username in session
			return jsonify({'msg':'login successful'})
	else:
		return jsonify({'msg': 'The username or password is incorrect'})
    

@app.route('/register', methods=['POST'])
def register():
    new_user = request.get_json() # store the json body request
    #below code literally check for juse username but who will check different password? aren't that leak already? 
    doc = usercollection.find_one({"username": new_user["username"]}) # check if user exist like
    #after checking logic
    if not doc:#pass
        usercollection.insert_one(new_user)
        return jsonify({'msg': 'User created successfully'}), 201
		
    else:#error given
        return jsonify({'msg': 'Username already exists'}), 409

    

@app.route('/update', methods=['POST'])
def update():
    data = request.json
    collection = db['DB1']
    result = collection.insert_one(data)
    if result.acknowledged:
        data = {
        "userinfo"         : data.get('userinfo')
        }
        collection.insert_one(data)
        return jsonify({'message': 'Registration successful'})
    else:
        return jsonify({'error': 'Please provide username and password'})
    
#view data seem it use dump? 
#-----------------------------end of Login & Registration

@app.route('/userinfo', methods=['POST'])
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
