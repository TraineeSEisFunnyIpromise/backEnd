# app.py
from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from pymongo import MongoClient
from compare import search_pattern
from chatgptreqsender import receiveinputtest
#JWT thingy
import jwt
import datetime
from functools import wraps

# instantiate the app
app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017')
db = client['Database1']
usercollection = db['DB1']
# enable CORS

CORS(app, resources={r'/*': {'origins': '*'}})
#JWT import
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'Your_Secret_Key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

@app.route('/')
def index():
    return render_template('EventList.html')
#Session * i should seperate this

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
			# access_token = create_access_token(identity=user_from_db['username']) # create jwt token
			return jsonify({'msg':'login successful'})
	else:
		return jsonify({'msg': 'The username or password is incorrect'})
    

@app.route('/register', methods=['POST'])
def register():
    new_user = request.get_json() # store the json body request
    doc = usercollection.find_one({"username": new_user["username"]}) # check if user exist
    if not doc:
        usercollection.insert_one(new_user)
        return jsonify({'msg': 'User created successfully'}), 201
		
    else:
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

@app.route('/userinfo')
@jwt_required
def profile():
	current_user = get_jwt_identity() # Get the identity of the current user
	user_from_db = usercollection.find_one({'username' : current_user})
	if user_from_db:
		del user_from_db['_id'], user_from_db['password'] # delete data we don't want to return
		return jsonify({'profile' : user_from_db }), 200
	else:
		return jsonify({'msg': 'Profile not found'}), 404

@app.route('/search', methods=['POST','GET'])
def search_products():
    if request.method == 'GET':  
        #Check word
        search_keyword = request.json
        #send to ChatGPT
        # receive_input(search_keyword)
        return usercollection.insert_one(search_keyword)
    elif request.method == 'POST':
        #send data back to request which '/search'
        search_keyword = request.json
        return receiveinputtest(search_keyword)
    else :
        return 'methods not allowed', 405


#start app down here _main_


if __name__ == '__main__':
    app.run()
