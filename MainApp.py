from flask import Flask
from account.Authentication import auth_bp  # Import the blueprint
from account.userinfo import userinformation_bp
from Reqandscrape.ScrapeController import search_bp
from flask_session import Session
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
# Initialize Flask-Session
# Configure Flask-Session (replace with your secret key)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_PERMANENT'] = False  # Set to True for persistent sessions (browser closed)
app.config['SESSION_TYPE'] = 'filesystem'  # Or use a database or Redis for storage
app.config['PERMANENT_SESSION_LIFETIME'] = 300
Session(app)

# Register the authentication blueprint
app.register_blueprint(auth_bp, url_prefix=('/auth'))
app.register_blueprint(userinformation_bp, url_prefix='/userinfo')
app.register_blueprint(search_bp, url_prefix='/search')
# enable CORS

# Your other application routes and logic here

if __name__ == '__main__':
  app.run(debug=True)
