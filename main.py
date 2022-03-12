import hashlib
import datetime
from flask import Flask, Response, make_response, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
from bson import json_util


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

jwt = JWTManager(app)
try:
	client = MongoClient("mongodb+srv://alex13:alex13@cluster0.48b4z.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
	db = client["usersdb"]
	users_collection = db["users"]
except Exception as e:
	print(e)

def validate_body(req_fields, body):
	body = list(body.keys())
	all_fields = 0
	for field in body:
		if field not in req_fields:
			return {"continue":False, "msg": "Only valid fields can be sent"}
		if field in req_fields:
			all_fields = all_fields + 1

	if all_fields != len(req_fields):
		return {"continue":False, "msg": "All fields are required"}

	return {"continue":True}

@app.route("/users/signup", methods=["POST"])
def signup():
	try:
		new_user = request.get_json()
		req_fields = ['username', 'password', 'name', 'age']
		is_valid = validate_body(req_fields=req_fields, body=new_user)

		if not is_valid['continue']:
			return jsonify({'msg': is_valid['msg'], 'fields': req_fields}), 400

		if new_user['age'] <= 0 or new_user['age'] > 120:
			return jsonify({'msg': 'Age cannot be greater than 120 or less than 1'}), 400

		new_user["password"] = hashlib.sha256(new_user["password"].encode("utf-8")).hexdigest() # encrpt password
		doc = users_collection.find_one({"username": new_user["username"]}) # check if user exist
		if not doc:
			users_collection.insert_one(new_user)
			return jsonify({'msg': 'User created successfully'}), 201
		else:
			return jsonify({'msg': 'Username already exists'}), 409
	except Exception as e:
		print(e)

@app.route("/users/login", methods=["POST"])
def login():
	try:
		login_details = request.get_json()
		req_fields = ['username', 'password']
		is_valid = validate_body(req_fields=req_fields, body=login_details)

		if not is_valid['continue']:
			return jsonify({'msg': is_valid['msg'], 'fields': req_fields}), 400
			
		user_from_db = users_collection.find_one({'username': login_details['username']})

		if user_from_db:
			encrpted_password = hashlib.sha256(login_details['password'].encode("utf-8")).hexdigest()
			if encrpted_password == user_from_db['password']:
				access_token = create_access_token(identity=user_from_db['username'])
				return jsonify(access_token=access_token), 200

		return jsonify({'msg': 'The username or password is incorrect'}), 401
	except Exception as e:
		print(e)

@app.route("/users/profile")
@jwt_required()
def profile():
	try:
		current_user = get_jwt_identity()
		user = users_collection.find_one({'username' : current_user})
		if user:
			del user['password']
			user = json_util.dumps(user)
			return Response(user, mimetype='application/json')
		else:
			return jsonify({'msg': 'Profile not found'}), 404
	except Exception as e:
		print(e)

@app.errorhandler(404)
def on_not_found(error):
    return make_response(jsonify({"msg":"Resource not found"}), 404)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=6000)