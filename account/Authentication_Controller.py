
from flask import Flask, Blueprint, request, jsonify, session
from flask_session import Session
from flask_cors import CORS
from account.Authentication import authentication,register_newuser,resetpassword_check
from database.databasemanager import check_database_status
from account.userinfo import sessioncheck
import json
#time stuff
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

    if check_database_status != False:
      result = authentication(usernameA,passA)
      print(type(result))
      print(result)
      if(type(result)!= str):
         return jsonify(result)
      
      if(result == "user not found"):
         return jsonify({'error':'user not found'})
      
      if(result == "incorrect password"):
         return jsonify({'error':'incorrect password'})
      
      if(result == "can not connect to database"):
         return jsonify({'error':'can not connect to database'})
    else: 
      return jsonify({'error':'Server is not avaliable'})


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
    print(new_user)
    register_newuser(new_user)
    return jsonify({'msg': 'User registered successfully'}),200


@auth_bp.route('/checkuser_reset', methods=['POST'])
def check_user():
    data = request.json
    if check_database_status == True:
      question = resetpassword_check(data['username'])
      return jsonify(question), 200
    else:
      return jsonify({'msg': 'database is down'}), 404



#---------------------------------- pure function around here--------------------------------
#check all data

#-------------------------------------------------------------------------------------
#-----------------------------end of Login & Registration-------------------------------------
Session(app)

if __name__ == '__main__':
    app.run()
