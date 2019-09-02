from flask import Blueprint, request, jsonify
from db.global_db import db
from db.models.user import User
from db.models.profile import Profile
from db.models.appointment import Appointment
from ..validation import isProperUsername, isProperPassword, isProperEmail
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

user_func = Blueprint('user_func', __name__)

@user_func.route('/user/<int:userid>', methods=['GET', 'PUT', 'DELETE'])
def user(userid):
	if request.method == 'GET':
		user = User.query.filter_by(userid=userid).first()
		if user is None: #if query is empty
			return 'None'
		id = user.userid
		username = user.username
		email = user.email
		createdDate = user.createdDate
		lastUpdated = user.lastUpdated
		isadmin = user.isadmin
		obj = jsonify(userid=id, username=username, email=email, 
					  createdDate=createdDate, lastUpdated=lastUpdated, 
					  isadmin=isadmin)
		return obj
	elif request.method == 'PUT':
		user = User.query.filter_by(userid=userid).first()
		if user is None: #if query is empty
			return 'Cannot update that user! It does not exist!'
		username = user.username if request.form.get('username') is None \
				or request.form['username'] is "" \
				else request.form['username']		
		if not isProperUsername(username):
			return 'Invalid username!'
		password = user.password if request.form.get('password') is None \
				or request.form['password'] is "" \
				else request.form['password']
		if not isProperPassword(password):
			return 'Invalid password!'
		email = user.email if request.form.get('email') is None \
				or request.form['email'] is "" \
				else request.form['email']
		if not isProperEmail(email):
			return 'Invalid email!'
		user.username = username
		user.password =  generate_password_hash(password)
		user.email = email
		user.lastUpdated = datetime.now()
		return 'User account has been updated!'
	elif request.method == 'DELETE':
		user = User.query.filter_by(userid=userid).first()
		if user is None: #if query is empty
			return 'Cannot delete that user! It does not exist!'
		profile = Profile.query.filter_by(userid=userid).first()
		#Need to make appointment available
		appointment = Appointment.query.filter_by(appointmentid=profile.appointmentid).first()
		if profile.appointmentid is not None:
			profile.appointmentid = None
			appointment.available = True
		db.session.delete(user)
		db.session.delete(profile)
		db.session.commit()
		return 'User account has been deleted!'
	else:
		return 'Unsupported HTTP method!'