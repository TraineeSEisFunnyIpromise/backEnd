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




def delete_account(username,password):
	user_from_db = access_database(username)
	if password == user_from_db['password']:
		delete_user(username)
		session.clear()
		return jsonify({'msg' : 'remove succesful' }), 200
	else:
		return jsonify({'msg': 'incorrect password'}), 400
	
