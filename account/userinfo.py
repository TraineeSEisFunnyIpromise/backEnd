# app.py
from flask import  jsonify, session
from database.databasemanager import update_user_aboutme,check_username,check_database_status,delete_user,update_password,access_database
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

def update_aboutme(username,data):
  if data!= '':
    if update_user_aboutme(username,data) == True:
      
      return 'update success'
    else:
      return 'update unsuccess'
  else:
    return 'data base is down'

def update_oldpassword(username,get_resetpassword): 
  if update_password(username,get_resetpassword) ==True:
      return 'Reset password successful'
  else:
    return 'Reset password unsuccessful'




def delete_account(username):

	if (check_username(username) == True):
		delete_user(username)
		session.clear()
		return jsonify({'msg' : 'remove succesful' }), True
	else:
		return jsonify({'msg': 'user not found'}), False
	
