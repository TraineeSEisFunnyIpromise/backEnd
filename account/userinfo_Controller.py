# app.py
from flask import  Blueprint, request, jsonify, session
from account.userinfo import delete_user,update_aboutme,check_database_status,update_oldpassword
# import userinfo function
#time stuff

# instantiate the app


userinformation_bp = Blueprint('userinfo', __name__)
#-------------------------------------import and setpu stuff ---------------------------------------


#----------------------------------------User info part--------------------------------------------
@userinformation_bp.route('/Update', methods=['POST'])
def update():
		data = request.json
		update_aboutme(data,data["username"])
		return jsonify({'message': 'Registration successful'})


     
@userinformation_bp.route('/Delete', methods=['POST'])
def delete_account():
	data = request.json
	if data["username"] != '':
		delete_user(data["username"],data["password"])
		return jsonify({'msg' : 'remove succesful' }), 200
	else:
		return jsonify({'msg': 'profile not found'}), 404

@userinformation_bp.route('/Resetpassword', methods=['POST'])
def reset_password():
	data = request.json
	username = session.get('user')
	if check_database_status == True:
		update_oldpassword(username,get_resetpassword=data["reset_password"])
		return jsonify({'msg' : 'remove succesful' }), 200
	else:
		return jsonify({'msg': 'database is down'}), 404

#start app down here _main_


