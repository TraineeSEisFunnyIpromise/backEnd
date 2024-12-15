
from flask import Flask, Blueprint, request, jsonify, session
from account.Authentication import authentication,register_newuser,resetpassword_check,resetpassword
from database.databasemanager import check_database_status
from account.userinfo import sessioncheck
#time stuff
# instantiate the app
app = Flask(__name__)

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


@auth_bp.route('/getuser', methods=['POST'])
def getuser():
    data = request.json
    if check_database_status == True:
      question = resetpassword_check(data['username'])
      return jsonify(question), 200
    else:
      return jsonify({'message': 'database is down'}), 404


@auth_bp.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.json
    if check_database_status == True:
      question = resetpassword(data['username'],data['answer'],data['password'])
      return jsonify(question), 200
    else:
      return jsonify({'message': 'database is down'}), 404

#---------------------------------- pure function around here--------------------------------
#check all data

#-------------------------------------------------------------------------------------
#-----------------------------end of Login & Registration-------------------------------------

if __name__ == '__main__':
    app.run()
