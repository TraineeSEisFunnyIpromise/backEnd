
from flask import Flask, Blueprint, request, jsonify, session
from flask_session import Session
from flask_cors import CORS
from pymongo import MongoClient
from account.Authentication import authentication,register_newuser
from database.databasemanager import check_database_status
from account.userinfo import sessioncheck
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

auth_bp = Blueprint('auth', __name__)

#-------------------------------------import and setpu stuff ---------------------------------------



#--------------------------------------------Login Part--------------------------------------------

@auth_bp.route('/login', methods=['POST'])
def login():
    login_details = request.get_json() # store the json body request
    usernameA = login_details['username']
    passA = login_details['password']

  # this is the most confused stuff that i ever done it look simple but tracking it
  #is the real challenge
    if check_database_status != False:
      authentication(usernameA,passA)

    else: #return server is fxck
      return jsonify({'msg':'Server is not avaliable'}),400


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
#---------------------------------------- Session status-------------------------------------------
@auth_bp.route('/sessioncheck',methods=['POST'])
def something():
    response = sessioncheck
    return jsonify(response)

#----------------------------------------register part--------------------------------------------
@auth_bp.route('/register', methods=['POST'])
def register():
    new_user = request.get_json() # store the json body request
    register_newuser(new_user)

#---------------------------------- pure function around here--------------------------------
#check all data

#-------------------------------------------------------------------------------------
#-----------------------------end of Login & Registration-------------------------------------
Session(app)

if __name__ == '__main__':
    app.run()
