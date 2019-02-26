#Need to modularize the Flask logic
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import re
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) #Need for access from other applications, such as Axios

#Check if the schema exists and create it if needed
engine = sqlalchemy.create_engine('mysql://root:8milerun@localhost')
engine.execute("CREATE SCHEMA IF NOT EXISTS `testdb`;")
engine.execute("USE testdb;")

#Configure app for testdb connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:8milerun@localhost/testdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Turn off annoying message
db = SQLAlchemy(app)

class User(db.Model):
	userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(16), unique=True, nullable=False)
	password = db.Column(db.String(512), unique=False, nullable=False)
	email = db.Column(db.String(80), unique=True, nullable=False)
	createdDate = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	lastUpdated = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	isadmin = db.Column(db.Boolean, nullable=False, default=False)

class Profile(db.Model):
	profileid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	firstname = db.Column(db.String(80), unique=False, nullable=True)
	lastname = db.Column(db.String(80), unique=False, nullable=True)
	ssn = db.Column(db.String(9), unique=False, nullable=True)
	phonenumber = db.Column(db.String(10), unique=False, nullable=True)
	birthdate = db.Column(db.DateTime, unique=False, nullable=True)
	createdDate = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
	lastUpdated = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
	userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)
	insuranceid = db.Column(db.Integer, db.ForeignKey('insurance.insuranceid'), nullable=True)
	appointmentid = db.Column(db.Integer, db.ForeignKey('appointment.appointmentid'), nullable=True)
	user = db.relationship('User', uselist=False, cascade='delete')
	appointment = db.relationship('Appointment', uselist=False, cascade='delete')
	insurance = db.relationship('Insurance', cascade='delete')

class Appointment(db.Model):
	appointmentid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	apptTime = db.Column(db.DateTime, nullable=True)
	available = db.Column(db.Boolean, nullable=False, default=True)
	createdDate = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	lastUpdated = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class Insurance(db.Model):
	insuranceid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	insurancecompany = db.Column(db.String(80), unique=False, nullable=False)
	groupnumber = db.Column(db.String(16), nullable=False)
	memberid = db.Column(db.String(16), unique=True, nullable=False)
	createdDate = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	lastUpdated = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

db.create_all()

def isProperUsername(username):
	if len(username) > 16 or len(username) < 3  \
	   or username.isnumeric() or username[0].isnumeric():
		return False
	else:
		return True

def isProperEmail(email):
	if len(email.split('@')) < 2 or len(email.split('.')) < 2:
		return False
	return True

def isProperPassword(password):
	if bool(re.search('[A-Z]', password)) and \
	   bool(re.search('[a-z]', password)) and \
	   bool(re.search('[0-9]', password)) and \
	   (len(password) >= 6 and len(password) <= 16):
		return True
	return False

def isValidSsn(ssn):
	return True if len(str(ssn)) is 9 and ssn.isnumeric() \
		   else False

def isValidPhonenumber(pnumber):
	return True if len(pnumber) is 10 and pnumber.isnumeric() \
		   else False

def isValidMemberid(memberid):
	return True if len(memberid) is 10 and memberid.isnumeric() \
		   else False

def isValidGroupNumber(groupnumber):
	return True if len(str(groupnumber)) > 2 and len(str(groupnumber)) <= 16 else False

def checkAvailable(available):
	if available is '1' or available is '0':
		return True
	return False

@app.route('/user/<int:userid>', methods=['GET', 'POST', 'DELETE'])
def user(userid):
	if request.method == 'GET':
		user = User.query.filter_by(userid=userid).first()
		if user is None: #if query is empty
			return 'None'
		id = user.userid
		username = user.username
		password = user.password
		email = user.email
		createdDate = user.createdDate
		lastUpdated = user.lastUpdated
		isadmin = user.isadmin
		obj = jsonify(id, username, password, email, createdDate, lastUpdated, isadmin)
		return obj
	elif request.method == 'POST':
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
		user.isadmin = isadmin
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

@app.route('/registerUser', methods=['POST'])
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

@app.route('/authenticate', methods=['POST'])
def authenticate():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		user = User.query.filter_by(username=username).first()
		if user is None:
			return 'User does not exist!'
		if (username != user.username) or \
		   (check_password_hash(user.password, password) is False):
		   return 'Authentication failed!'
		return 'Authentication succeeded!'
	return 'Unsupported HTTP method!'

@app.route('/toggleAdmin/<int:userid>', methods=['POST'])
def toggleAdmin(userid):
	if request.method == 'POST':
		user = User.query.filter_by(userid=userid).first()
		print(user.isadmin)
		user.isadmin = True if user.isadmin is False else False
		db.session.commit()
		return 'User\'s administrative privileges have been changed!'
	return 'Unsupported HTTP method!'

@app.route('/profile/<int:userid>', methods=['GET', 'POST'])
def profile(userid):
	if request.method == 'GET':
		profile = Profile.query.filter_by(userid=userid).first()
		if profile is None: #if query is empty
			return 'None'
		profileid = profile.profileid
		firstname = profile.firstname
		lastname = profile.lastname
		ssn = profile.ssn
		phonenumber = profile.phonenumber
		birthdate = profile.birthdate
		createdDate = profile.createdDate
		lastUpdated = profile.lastUpdated
		userid = profile.userid
		insuranceid = profile.insuranceid
		appointmentid = profile.appointmentid
		obj = jsonify(profileid, firstname, lastname,
					  ssn, phonenumber, birthdate,
					  createdDate, lastUpdated, userid,
					  insuranceid, appointmentid)
		return obj
	elif request.method == 'POST':
		profile = Profile.query.filter_by(userid=userid).first()
		if profile is None: #if query is empty
			return 'Cannot update that profile! It does not exist!'
		firstname = profile.firstname if request.args.get('firstname') is None \
				or request.args['firstname'] is "" \
				else request.args['firstname']		
		lastname = profile.lastname if request.args.get('lastname') is None \
				or request.args['lastname'] is "" \
				else request.args['lastname']	
		ssn = profile.ssn if request.args.get('ssn') is None \
				or request.args['ssn'] is "" \
				else request.args['ssn']	
		if not isValidSsn(ssn):
			return 'Invalid SSN!'
		phonenumber = profile.phonenumber if request.args.get('phonenumber') is None \
				or request.args['phonenumber'] is "" \
				else request.args['phonenumber']
		if not isValidPhonenumber(phonenumber):
			return 'Invalid phone number!'
		birthdate = profile.birthdate if request.args.get('birthdate') is None \
				or request.args['birthdate'] is "" \
				else request.args['birthdate']
		if request.args.get('insuranceid') is not None:
			insuranceid = request.args['insuranceid']
			if Insurance.query.filter_by(insuranceid=insuranceid).first() is None:
				return 'No insurances exist with that insuranceid!'
			profile.insuranceid = insuranceid
		if request.args.get('appointmentid') is not None:
			appointmentid = request.args['appointmentid']
			if Appointment.query.filter_by(appointmentid=appointmentid).first() is None:
				return 'No appointments exist with that appointmentid!'
		profile.appointmentid = appointmentid
		profile.firstname = firstname
		profile.lastname = lastname
		profile.ssn = ssn
		profile.phonenumber = phonenumber
		profile.birthdate = birthdate
		profile.lastUpdated = datetime.now()
		db.session.commit()
		return 'User profile has been updated!'
	else:
		return 'Unsupported HTTP method!'

@app.route('/appointment/<int:appointmentid>', methods=['GET', 'POST', 'DELETE'])
def appointment(appointmentid):
	if request.method == 'GET':
		appointment = Appointment.query.filter_by(appointmentid=appointmentid).first()
		if appointment is None: #if query is empty
			return 'None'
		appointmentid = appointment.appointmentid
		apptTime = appointment.apptTime
		available = appointment.available
		createdDate = appointment.createdDate
		lastUpdated = appointment.lastUpdated
		obj = jsonify(appointmentid, apptTime, available,
					  createdDate, lastUpdated)
		return obj
	elif request.method == 'POST':
		appointment = Appointment.query.filter_by(appointmentid=appointmentid).first()
		if appointment is None: #if query is empty
			return 'Cannot update that appointment! It does not exist!'
		apptTime = appointment.apptTime if request.args.get('apptTime') is None \
				or request.args['apptTime'] is "" \
				else request.args['apptTime']		
		available = appointment.available if request.args.get('available') is None \
				or request.args['available'] is "" \
				else request.args['available']
		if not checkAvailable(available):
			return 'Wrong format for availability'
		available = False if available is 0 else True
		appointment.apptTime = apptTime
		appointment.available = available
		appointment.lastUpdated = datetime.now()
		db.session.commit()
		return 'Appointment has been updated!'
	elif request.method == 'DELETE':
		appointment = Appointment.query.filter_by(appointmentid=appointmentid).first()
		if appointment is None: #if query is empty
			return 'Cannot delete that appointment! It does not exist!'
		#Remove appointmentid from user profiles
		profile = Profile.query.filter_by(appointmentid=appointmentid).first()
		if profile.appointmentid is not None:
			profile.appointmentid = None
		db.session.delete(appointment)
		db.session.commit()
		return 'Appointment has been deleted!'
	else:
		return 'Unsupported HTTP method!'

@app.route('/createAppt', methods=['POST'])
def createAppt():
	if request.method == 'POST':
		if len(request.args) is 0:
			return 'Request was empty!'
		apptTime = request.args['apptTime']
		createdDate = datetime.now()
		lastUpdated = datetime.now()
		appointment = Appointment(apptTime=apptTime,
								  createdDate=createdDate, lastUpdated=lastUpdated)
		db.session.add(appointment)
		db.session.commit()
		return 'Registration success!'
	else:
		return 'Unsupported HTTP method!'

@app.route('/makeAppointment/<int:userid>', methods=['POST'])
def makeAppointment(userid):
	if request.method == 'POST':
		appointmentid = request.args['appointmentid']
		appointment = Appointment.query.filter_by(appointmentid=appointmentid).first()
		if appointment.available is False:
			return 'That apointment is not available!'
		appointment.available = False
		profile = Profile.query.filter_by(userid=userid).first()
		profile.appointmentid = appointmentid
		db.session.commit()
		return 'Appointment successfully booked.'
	return 'Unsupported HTTP method!'

@app.route('/cancelAppointment/<int:userid>', methods=['POST'])
def cancelAppointment(userid):
	if request.method == 'POST':
		appointmentid = request.args['appointmentid']
		appointment = Appointment.query.filter_by(appointmentid=appointmentid).first()
		if appointment.available is True:
			return 'That appointment is already available.'
		appointment.available = True
		profile = Profile.query.filter_by(userid=userid).first()
		profile.appointmentid = None
		db.session.commit()
		return 'Appointment canceled!'
	return 'Unsupported HTTP method!'

@app.route('/insurance/<int:insuranceid>', methods=['GET', 'POST', 'DELETE'])
def insurance(insuranceid):
	if request.method == 'GET':
		insurance = Insurance.query.filter_by(insuranceid=insuranceid).first()
		if insurance is None: #if query is empty
			return 'None'
		insuranceid = insurance.insuranceid
		insurancecompany = insurance.insurancecompany
		groupnumber = insurance.groupnumber
		memberid = insurance.memberid
		createdDate = insurance.createdDate
		lastUpdated = insurance.lastUpdated
		obj = jsonify(insuranceid, insurancecompany, groupnumber,
					  memberid, createdDate, lastUpdated)
		return obj
	elif request.method == 'POST':
		insurance = Insurance.query.filter_by(insuranceid=insuranceid).first()
		if insurance is None: #if query is empty
			return 'Cannot update that insurance company! It does not exist!'
		insurancecompany = insurance.insurancecompany if request.args.get('insurancecompany') is None \
				or request.args['insurancecompany'] is "" \
				else request.args['insurancecompany']		
		groupnumber = insurance.groupnumber if request.args.get('groupnumber') is None \
				or request.args['groupnumber'] is "" \
				else request.args['groupnumber']	
		memberid = insurance.memberid if request.args.get('memberid') is None \
				or request.args['memberid'] is "" \
				else request.args['memberid']
		insurance.insurancecompany = insurancecompany
		insurance.groupnumber = groupnumber
		insurance.memberid = memberid
		insurance.lastUpdated = datetime.now()
		db.session.commit()
		return 'Insurance has been updated!'
	elif request.method == 'DELETE':
		insurance = Insurance.query.filter_by(insuranceid=insuranceid).first()
		if insurance is None: #if query is empty
			return 'Cannot delete that insurance company! It does not exist!'
		#Remove insuranceid from all user profiles
		profile = Profile.query.filter_by(insuranceid=insuranceid).all()
		if profile is not None:
			for p in profile:
				p.insuranceid = None
		db.session.delete(insurance)
		db.session.commit()
		return 'Insurance has been deleted!'
	else:
		return 'Unsupported HTTP method!'

@app.route('/createInsurance', methods=['POST'])
def createInsurance():
	if request.method == 'POST':
		if len(request.args) is 0:
			return 'Request was empty!'
		insurancecompany = request.args['insurancecompany']
		groupnumber = request.args['groupnumber']
		if not isValidGroupNumber(groupnumber):
			return 'Invalid Group Number!'
		memberid = request.args['memberid']
		if not isValidMemberid(memberid):
			return 'Invalid Member ID!'
		createdDate = datetime.now()
		lastUpdated = datetime.now()
		insurance = Insurance(insurancecompany=insurancecompany, groupnumber=groupnumber,
							  memberid=memberid, createdDate=createdDate, lastUpdated=lastUpdated)
		db.session.add(insurance)
		db.session.commit()
		return 'Registration success!'
	else:
		return 'Unsupported HTTP method!'

@app.route('/registerInsurance/<int:userid>', methods=['POST'])
def registerInsurance(userid):
	if request.method == 'POST':
		insuranceid = request.args['insuranceid']
		profile = Profile.query.filter_by(userid=userid).first()
		if str(profile.insuranceid) == insuranceid:
			return 'That insurance company is already registered to that user!'
		profile.insuranceid = insuranceid
		db.session.commit()
		return 'Insurance successfully applied.'
	return 'Unsupported HTTP method!'

@app.route('/deregisterInsurance/<int:userid>', methods=['POST'])
def deregisterInsurance(userid):
	if request.method == 'POST':
		profile = Profile.query.filter_by(userid=userid).first()
		if profile.insuranceid is None:
			return 'This user profile does not have any insurance!'
		profile.insuranceid = None
		db.session.commit()
		return 'Insurance successfully deregistered!'
	return 'Unsupported HTTP method!'

if __name__ == '__main__':
	app.run(debug=True)