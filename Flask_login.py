# app.py
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

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
    username = request.form.get('username')
    password = request.form.get('password')

    # Replace the following code with your own authentication logic
    if username == 'admin' and password == 'password':
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'error': 'Invalid username or password'})

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    # Replace the following code with your own registration logic
    if username and password:
        return jsonify({'message': 'Registration successful'})
    else:
        return jsonify({'error': 'Please provide username and password'})
    
@app.route('/userinfo')
def index():
    return render_template('userinfo.html')

@app.route('/test', methods=['POST'])
def handle_data():
    data = request.get_json()
    # Access the sent data using data['key'] where 'key' is the key in the sent data object
    received_data = data['data']
    # Process the received data as needed
    # ...

    # Return a response if needed
    return jsonify({'message': 'Data received successfully'})

if __name__ == '__main__':
    app.run()
