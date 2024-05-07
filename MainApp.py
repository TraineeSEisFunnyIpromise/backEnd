# app.py
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from compare import search_pattern
# from chatgptreqsender import receive_input
import pymongo

#JWT thingy
import jwt
from datetime import datetime, timedelta
from functools import wraps

# instantiate the app
app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017')
db = client['database1']
addsearchkeyword = db['DB1']
# enable CORS

CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/')
def index():
    return render_template('EventList.html')
#Session * i should seperate this

#Login & Register Section
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Replace the following code with your own authentication logic
    if username == 'admin' and password == 'admin1':
        print(username,password)
        return jsonify({'message': 'Login successful'})
    else:
        print(username,password)
        return jsonify({'error': 'Invalid username or password'})
    

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    collection = db['DB1']
    result = collection.insert_one(data)
    if result.acknowledged:
        data = {
        "name"        : data.get('name'),
        "password"    : data.get('password'),
        "info"         : data.get('info')
        }
        print(data)
        collection.insert_one(data)
        print(data)
        return jsonify({'message': 'Registration successful'})
    else:
        print(data)
        return jsonify({'error': 'Please provide username and password'})
    

@app.route('/update', methods=['POST'])
def update():
    data = request.json
    collection = db['DB1']
    result = collection.insert_one(data)
    if result.acknowledged:
        data = {
        "name"        : data.get('name'),
        "password"    : data.get('password'),
        "info"         : data.get('info')
        }
        print(data)
        collection.insert_one(data)
        return jsonify({'message': 'Registration successful'})
    else:
        print(data)
        return jsonify({'error': 'Please provide username and password'})
    
#view data seem it use dump? 
#-----------------------------end of Login & Registration

@app.route('/userinfo')
def yeet():
    return render_template('userinfo.html')

@app.route('/search', methods=['POST','GET'])
def search_products():
    if request.method == 'GET':  
        #Check word
        search_keyword = request.json
        #send to ChatGPT
        # receive_input(search_keyword)
        return addsearchkeyword.insert_one(search_keyword)
    elif request.method == 'POST':
        #send data back to request which '/search'

        return 0
    else :
        return 'methods not allowed', 405
    

@app.route('/search_test', methods=['POST','GET'])
def search_test():
    if request.method == 'GET':  

        return print("fronend send to back")
    elif request.method == 'POST':
        #send data back to request which '/search'
        return 0
    else :
        return 'methods not allowed', 405
    



#start app down here _main_


if __name__ == '__main__':
    app.run()
