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
	data = request.form
	if request.method == 'POST':
		if len(data) is 0:
			return 'Request was empty!'
		username = data['username']
		if not isProperUsername(username):
			return 'Invalid username!'
		password = data['password']
		if not isProperPassword(password):
			return 'Invalid password!'
		password = generate_password_hash(password)
		email = data['email']
		if not isProperEmail(email):
			return 'Invalid email!'
		createdDate = datetime.now()
		lastUpdated = datetime.now()
		if User.query.filter_by(username=username).first() is not None:
			return 'A user already exists with the username!'
		elif User.query.filter_by(email=email).first() is not None:
			return 'A user already exists with the email!'
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
			return 'Registration success!'
		return 'Registration failed!'
	else:
		return 'Unsupported HTTP method!'