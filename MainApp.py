from flask import Flask
from Authentication import auth_bp  # Import the blueprint
from flask_session import Session
from flask_cors import CORS

app = Flask(__name__)
# Initialize Flask-Session
# Configure Flask-Session (replace with your secret key)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_PERMANENT'] = False  # Set to True for persistent sessions (browser closed)
app.config['SESSION_TYPE'] = 'filesystem'  # Or use a database or Redis for storage
app.config['PERMANENT_SESSION_LIFETIME'] = 300
Session(app)

# Register the authentication blueprint
app.register_blueprint(auth_bp)
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
# Your other application routes and logic here

if __name__ == '__main__':
  app.run(debug=True)
