
from flask import  session,jsonify
from database.databasemanager import check_username,access_database,add_new_user,check_database_status,update_password
#time stuff
import uuid
from datetime import datetime, timedelta
# instantiate the app


#-------------------------------------import and setpu stuff ---------------------------------------


#--------------------------------------------Login Part-------------------------------------------

def authentication(username, password):
	#check database status
      if check_database_status() != False :
          #access account data according to name
          print("username" + username)
          print("password" + password)
          something = check_username(username)
          print(something)
          if check_username(username) != False:
            user_from_db = access_database(username)
            #straight up check empty and password kek
            print("detected user" )
            if(user_from_db != "Database connection timed out"):
                if ((user_from_db != None) and (password == user_from_db['password']) == True):
                  result = user_from_db
                  session['username'] = username
                  result['_id'] = str(result['_id'])
                  session['_id'] = user_from_db['_id']
                  print("login session info")
                  print(session)
                  return result
                else:
                  result = 'Incorrect passwords'
                  return result 
            else:
                result = 'can not connect to database'
                return result
          else:
              result = 'user not found'
              return  result
      else:
            result = 'The server is down'
            return result

#---------------------------------------- reset password section -------------------------------------------
def resetpassword(username,get_resetanswer,get_resetpassword):
  userdata = access_database(username)
  answer_for_resetpassword = userdata["answer_for_reset"]
  if (get_resetanswer ==  answer_for_resetpassword) == True:
        update_password(username,get_resetpassword)
        return 'success'
  else:
    return 'unsuccess'
  

#----------------------------------------register part--------------------------------------------
def register_newuser(data):
    new_user = data # store the json body request
    user_id = str(uuid.uuid4())
    #find user
    doc = check_username(new_user["username"]) # check if user exist like
    #after checking no same username detected
    print("checkresult : ")
    print(doc)
    if doc == False:#not detect user
        new_user['user_id'] = user_id
        print(new_user)
        add_new_user(new_user["username"],new_user)
        if check_username(new_user["username"]) == True:
          return  'User created successfully'
        else:
          return 'bad database'
    else:
        return 'Username already exists'

def resetpassword_check(username):
  if (check_username(username)) == True:
        userdata = access_database(username)
        question = userdata["question_for_reset"]
        return question
  else:
    return 'user not found'
  
#-----------------------------------tempt fix user info--------------------------------------------------

def userinfo():
	    # Check if the user is logged in by verifying the session
    print("session username")
    print(session['username'])
    if 'username' in session:
        username = session['username']
        
        # Find the user in the database using the username from the session
        if check_database_status == True:
          user = access_database(username)
        if user == True:
            # Return user data (excluding sensitive information)
            return jsonify({'username': user['username'], 'about me': user.get('about me', 'No information available')}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    else:
        # User is not logged in or session has expired
        return jsonify({'error': 'Unauthorized'}), 401
    
def sessioncheck():
			username = session.get('user')
				# Calculate time left until session expires (server-side)
			session_start_time = session.get('start_time')
			now = datetime.utcnow
			duration_left = session_start_time + timedelta() - now
			response = username + "  " + duration_left
			return jsonify(response)
    
#-----------------------------end of Login & Registration-------------------------------------
