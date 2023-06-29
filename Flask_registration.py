# app.py
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    # Replace the following code with your own registration logic
    if username and password:
        return jsonify({'message': 'Registration successful'})
    else:
        return jsonify({'error': 'Please provide username and password'})

if __name__ == '__main__':
    app.run()
