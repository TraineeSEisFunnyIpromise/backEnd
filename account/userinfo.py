# app.py
from flask import  jsonify, session
from database.databasemanager import update_user_aboutme,check_database_status,access_database,delete_user,update_password
#time stuff
from datetime import datetime, timedelta
# instantiate the app

#-------------------------------------import and setpu stuff ---------------------------------------

#                                        Session status

def sessioncheck():
			username = session.get('user')
				# Calculate time left until session expires (server-side)
			session_start_time = session.get('start_time')
			now = datetime.utcnow
			duration_left = session_start_time + timedelta() - now
			response = username + "  " + duration_left
			return jsonify(response)

#----------------------------------------User info part--------------------------------------------

def update_aboutme(data):
  username = session.get('user')
  if data["send" != '']:
    if check_database_status() == True:
      update_user_aboutme(data,username)
    else:
      return
    return jsonify({'message': 'Registration successful'})
  else:
    return jsonify({'error': 'Please provide username and password'})


def update_oldpassword(username,get_resetpassword): 
  if get_resetpassword != '':
        update_password(username,get_resetpassword)
  else:
    return jsonify({'error': 'Please providepassword'})
  return jsonify({'message': 'Reset password successful'})




def delete_account(username,password):
	user_from_db = access_database(username)
	if password == user_from_db['password']:
		delete_user(username)
		return jsonify({'msg' : 'remove succesful' }), 200
	else:
		return jsonify({'msg': 'incorrect password'}), 400
	
