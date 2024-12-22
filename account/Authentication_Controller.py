
from flask import Blueprint, request, jsonify, session
from account.Authentication import authentication,register_newuser,resetpassword_check,resetpassword,sessioncheck
from database.databasemanager import check_database_status
from account.userinfo import access_database
from datetime import datetime, timedelta
#time stuff
# instantiate the app


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
      print("session info at login")
      print(session)
      print(result)
      print(type(result))
      print(result)
      if(type(result)!= str):
         return jsonify(result),202
      else:
         return jsonify({'message':result})
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
    result = register_newuser(new_user)
    if result == "User created successfully":
      return jsonify({'message': 'User registered successfully'})
    else:
      return jsonify({'message': 'Username already exists'})


@auth_bp.route('/searchinguser', methods=['POST'])
def getuser():
    data = request.json
    if check_database_status == True:
      question = resetpassword_check(data['username'])
      if question != 'user not found':
        return jsonify(question), 200
      else: 
         return jsonify({'message': 'user not found'})
    else:
      return jsonify({'message': 'database is down'})


@auth_bp.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.json
    if check_database_status == True:
      question = resetpassword(data['username'],data['answer'],data['password'])
      return jsonify(question), 200
    else:
      return jsonify({'message': 'database is down'})


#---------------------------------- temp userinfo fix around here--------------------------------
#legit confused why from this function to different function it couldn't access possibly that
#from authen to authen control it can cross from userinfo control to authen control
@auth_bp.route('/Information', methods=['POST'])
def get_userinfo():
	    # Check if the user is logged in by verifying the session
    user = session.get('user_id')
    print("session information at userinfo")
    print(session.get('username'))
    print(user)
    
    if user is not None:

        # Find the user in the database using the username from the session
        data = access_database(user)
        
        if user is not None:
            # Return user data (excluding sensitive information)
            return data, 200
        else:
            return jsonify({'error': 'User not found'}), 404
    else:
        # User is not logged in or session has expired
        return jsonify({'error': 'Unauthorized'}), 400
    
#                                        Session status
@auth_bp.route('/Sessioncheck',methods=['POST'])
def sessioncheck():
			username = session.get('user_id')
				# Calculate time left until session expires (server-side)
			session_start_time = session.get('start_time')
			now = datetime.utcnow
			duration_left = session_start_time + timedelta() - now
			response = username + "  " + duration_left
			return jsonify(response)
#-------------------------------------------------------------------------------------
#-----------------------------end of Login & Registration-------------------------------------
