from flask import Blueprint, request, jsonify
from db.global_db import db
from db.models.user import User
from db.models.profile import Profile
from db.models.appointment import Appointment
from ..validation import isProperEmail, isProperPassword
from werkzeug.security import generate_password_hash
from datetime import datetime

user_func = Blueprint('user_func', __name__)

@user_func.route('/user/<int:userid>', methods=['GET', 'PUT', 'DELETE'])
def user(userid):
	if request.method == 'GET':
		user = User.query.filter_by(userid=userid).first()
		if user is None: #if query is empty
			return jsonify('None')
		id = user.userid
		email = user.email
		createdDate = user.createdDate
		lastUpdated = user.lastUpdated
		isadmin = user.isadmin
		sec_ques_num = user.sec_ques_num
		obj = jsonify(userid=id, email=email, createdDate=createdDate,
					  lastUpdated=lastUpdated, isadmin=isadmin, sec_ques_num=sec_ques_num)
		return obj
	elif request.method == 'PUT':
		user = User.query.filter_by(userid=userid).first()
		if user is None: #if query is empty
			return jsonify('Cannot update that user! It does not exist!')
		data = request.get_json()
		email = user.email if data.get('email') is None \
			else data.get('email')
		if not isProperEmail(email):
			return jsonify('Invalid email!')
		password = user.password if data.get('password') is None \
			else data.get('password')
		if not isProperPassword(password):
			return jsonify('Invalid password!')
		user.email = email
		user.password =  generate_password_hash(password, 'sha256')
		user.lastUpdated = datetime.now()
		db.session.commit()
		return jsonify('User account has been updated!')
	elif request.method == 'DELETE':
		user = User.query.filter_by(userid=userid).first()
		if user is None: #if query is empty
			return jsonify('Cannot delete that user! It does not exist!')
		profile = Profile.query.filter_by(userid=userid).first()
		#Need to make appointment available
		appointment = Appointment.query.filter_by(appointmentid=profile.appointmentid).first()
		if profile.appointmentid is not None:
			profile.appointmentid = None
			appointment.available = True
		db.session.delete(user)
		db.session.delete(profile)
		db.session.commit()
		return jsonify('User account has been deleted!')
