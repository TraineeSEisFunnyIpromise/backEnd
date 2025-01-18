# app.py
from flask import  Blueprint, request, jsonify, session
from account.userinfo import delete_user,update_aboutme,check_database_status,update_oldpassword,access_database
# import userinfo function
#time stuff

# instantiate the app


userinformation_bp = Blueprint('userinfo', __name__)
#-------------------------------------import and setpu stuff ---------------------------------------


#----------------------------------------User info part--------------------------------------------
@userinformation_bp.route('/Update', methods=['POST'])
def update():
		data = request.json
		print(data)
		print(data["aboutme"])
		result = update_aboutme(data['username'],data["aboutme"])
		return jsonify({'message': result})


     
@userinformation_bp.route('/Delete', methods=['POST'])
def delete_account():
	data = request.json
	password_fromfront = data["password"]
	datafromdb = access_database(data["username"])
	password_fromdb = datafromdb["password"]

	if(password_fromfront == password_fromdb):
			if delete_user(data["username"]) ==True:
			
				return jsonify({'msg' : 'remove successful' }), 200
			else:
				return jsonify({'msg': 'remove unsuccessful'}), 404
	else:
		return jsonify({'msg': 'remove unsuccessful'}), 404

	


@userinformation_bp.route('/PasswordUpdate', methods=['POST'])
def updatepass():
	data = request.json
	username = data['username']
	if check_database_status() == True:
		print("update pass method")
		result = update_oldpassword(username,get_resetpassword=data["password"])
		print(result)
		return jsonify(result), 200
	else:
		return jsonify({'msg': 'database is down'}),400

#start app down here _main_


