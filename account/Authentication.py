
from flask import Flask, jsonify, session
from flask_session import Session
from flask_cors import CORS
from database.databasemanager import check_username,access_database,add_new_user,check_database_status,update_password
#time stuff
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


#-------------------------------------import and setpu stuff ---------------------------------------


#--------------------------------------------Login Part-------------------------------------------

def authentication(username, password):
	#check database status
      if check_database_status != False :
          #access account data according to name
          print(username)
          if check_username(username) != '':
            user_from_db = access_database(username)
            #straight up check empty and password kek
            print(user_from_db)
            if ((user_from_db != None) and (password == user_from_db['password']) == True):
              result = user_from_db
              session['username'] = username
              result["_id"] = str(result["_id"])
              return result
            else:
              return jsonify({'msg': 'Incorrect passwords'}),400
          else:
              return jsonify({'msg': 'no user exist'}),400
      else:
            return jsonify({'msg': 'The database is down!!!'}),504

#---------------------------------------- reset password section -------------------------------------------
def resetpassword(username,get_resetanswer,get_resetpassword):
  userdata = access_database(username)
  answer_for_resetpassword = userdata["answer_for_reset"]
  if (get_resetanswer ==  answer_for_resetpassword) == True:
        update_password(username,get_resetpassword)
  else:
    return jsonify({'error': 'Please provide correct username and answer'})
  return jsonify({'message': 'Reset password successful'})

#----------------------------------------register part--------------------------------------------
def register_newuser(data):
    new_user = data # store the json body request
    user_id = str(uuid.uuid4())
    #find user
    print("register")
    doc = check_username(new_user["username"]) # check if user exist like
    #after checking no same username detected
    print(doc)
    if doc == True:#pass
        new_user['user_id'] = user_id
        print(new_user)
        add_new_user(new_user["username"],new_user)
        return jsonify({'msg': 'User created successfully'}), 201
		
    else:#error given
        return jsonify({'msg': 'Username already exists'}), 409

def resetpassword_check(username):
  if (check_username(username)) == True:
        userdata = access_database(username)
        question = userdata["question_for_reset"]
        return question
  else:
    return jsonify({'error': 'target user is not exist'})
  
#-------------------------------------------------------------------------------------
#-----------------------------end of Login & Registration-------------------------------------
Session(app)

if __name__ == '__main__':
    app.run()
