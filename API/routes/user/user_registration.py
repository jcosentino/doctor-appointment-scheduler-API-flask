from flask import Blueprint, request, jsonify
from db.global_db import db
from db.models.user import User
from db.models.profile import Profile
from ..validation import isProperEmail, isProperPassword,\
						 isProperSecurityQuestion, isProperSecurityAnswer
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

user_registration = Blueprint('user_registration', __name__)

@user_registration.route('/registerUser', methods=['POST'])
def registerUser():
	data = request.get_json()
	if request.method == 'POST':
		if len(data) == 0:
			return jsonify('Request was empty!')
		email = data.get('email')
		if not isProperEmail(email):
			return jsonify('Invalid email!')
		password = data.get('password')
		if not isProperPassword(password):
			return jsonify('Invalid password!')
		password = generate_password_hash(password, 'sha256')
		sec_ques_num = data.get('sec_ques_num')
		if not isProperSecurityQuestion(sec_ques_num):
			return jsonify('Security question must be between and including 1 and 3.')
		sec_ques_ans = data.get('sec_ques_ans')
		if not isProperSecurityAnswer(sec_ques_ans):
			return jsonify('Security answer must be between and including 6 and 26 characters.')
		sec_ques_ans = generate_password_hash(sec_ques_ans, 'sha256')
		createdDate = datetime.now()
		lastUpdated = datetime.now()
		if User.query.filter_by(email=email).first() is not None:
			return jsonify('A user already exists with the email!')
		else:
			user = User(email=email, 
						password=password,
						createdDate=createdDate,
						lastUpdated=lastUpdated,
						sec_ques_num=sec_ques_num,
						sec_ques_ans=sec_ques_ans)
			db.session.add(user)
			db.session.commit()
			userid = User.query.filter_by(email=email).first().userid
			profile = Profile(createdDate=createdDate, 
							  lastUpdated=lastUpdated,
							  userid=userid)
			db.session.add(profile)
			db.session.commit()
			return jsonify('Registration success!')
