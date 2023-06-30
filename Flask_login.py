# app.py
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

# instantiate the app
app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['database1']

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})



@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/')
def index():
    return render_template('EventList.html')

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
        print(data)
        return jsonify({'message': 'Registration successful'})
    else:
        print(data)
        return jsonify({'error': 'Please provide username and password'})
    
@app.route('/userinfo')
def yeet():
    return render_template('userinfo.html')



@app.route('/testDB', methods=['POST'])
def handle_data():
    data = request.get_json()
    # Access the sent data using data['key'] where 'key' is the key in the sent data object
    username = "gda"
    password = "gda"
    collection = db['DB1']
    result = collection.insert_one(username,password)
    # Process the received data as needed
    # ...

    # Return a response if needed
    return jsonify({'message': 'Data received successfully'})

if __name__ == '__main__':
    app.run()
