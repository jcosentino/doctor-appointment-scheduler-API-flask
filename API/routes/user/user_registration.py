from flask import Blueprint, request, jsonify
from db.global_db import db
from db.models.user import User
from db.models.profile import Profile
from ..validation import isProperUsername, isProperPassword, isProperEmail
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

user_registration = Blueprint('user_registration', __name__)

@user_registration.route('/registerUser', methods=['POST'])
def registerUser():
	data = request.get_json()
	if request.method == 'POST':
		if len(data) is 0:
			return jsonify('Request was empty!')
		username = data.get('username')
		if not isProperUsername(username):
			return jsonify('Invalid username!')
		password = data.get('password')
		if not isProperPassword(password):
			return jsonify('Invalid password!')
		password = generate_password_hash(password)
		email = data.get('email')
		if not isProperEmail(email):
			return jsonify('Invalid email!')
		createdDate = datetime.now()
		lastUpdated = datetime.now()
		if User.query.filter_by(username=username).first() is not None:
			return jsonify('A user already exists with the username!')
		elif User.query.filter_by(email=email).first() is not None:
			return jsonify('A user already exists with the email!')
		else:
			user = User(username=username, 
						password=password, 
						email=email, 
						createdDate=createdDate, 
						lastUpdated=lastUpdated)
			db.session.add(user)
			db.session.commit()
			userid = User.query.filter_by(username=username).first().userid
			profile = Profile(createdDate=createdDate, 
							  lastUpdated=lastUpdated,
							  userid=userid)
			db.session.add(profile)
			db.session.commit()
			return jsonify('Registration success!')
		return jsonify('Registration failed!')
	else:
		return jsonify('Unsupported HTTP method!')