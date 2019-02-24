#Need to modularize the Flask logic
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import re
import sqlalchemy

app = Flask(__name__)
CORS(app) #Need for access from other applications, such as Axios

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
	password = db.Column(db.String(16), unique=False, nullable=False)
	email = db.Column(db.String(80), unique=True, nullable=False)
	createdDate = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	lastUpdated = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class Profile(db.Model):
	profileid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	firstname = db.Column(db.String(80), unique=False, nullable=False)
	lastname = db.Column(db.String(80), unique=False, nullable=False)
	ssn = db.Column(db.String(9), unique=False, nullable=False)
	phonenumber = db.Column(db.String(10), unique=False, nullable=False)
	birthdate = db.Column(db.DateTime, unique=False, nullable=False)
	createdDate = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	lastUpdated = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)
	insuranceid = db.Column(db.Integer, db.ForeignKey('insurance.insuranceid'), nullable=True)

class Appointment(db.Model):
	appointmentid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	apptTime = db.Column(db.DateTime, nullable=True)
	available = db.Column(db.Boolean, nullable=False, default=True)
	createdDate = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	lastUpdated = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=True)

class Insurance(db.Model):
	insuranceid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	insurancecompany = db.Column(db.String(80), unique=False, nullable=False)
	groupnumber = db.Column(db.Integer, nullable=False)
	memberid = db.Column(db.String(10), unique=True, nullable=False)
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
	   (len(password) >=6 and len(password) <= 16):
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
		obj = jsonify(id, username, password, email, createdDate, lastUpdated)
		return obj
	elif request.method == 'POST':
		user = User.query.filter_by(userid=userid).first()
		if user is None: #if query is empty
			return 'Cannot update that user! It does not exist!'
		username = user.username if request.args.get('username') is None \
				or request.args['username'] is "" \
				else request.args['username']		
		if not isProperUsername(username):
			return 'Invalid username!'
		password = user.password if request.args.get('password') is None \
				or request.args['password'] is "" \
				else request.args['password']
		if not isProperPassword(password):
			return 'Invalid password!'
		email = user.email if request.args.get('email') is None \
				or request.args['email'] is "" \
				else request.args['email']
		if not isProperEmail(email):
			return 'Invalid email!'
		user.username = username
		user.password = password
		user.email = email
		user.lastUpdated = datetime.now()
		db.session.commit()
		return 'User account has been updated!'
	elif request.method == 'DELETE':
		user = User.query.filter_by(userid=userid).first()
		if user is None: #if query is empty
			return 'Cannot delete that user! It does not exist!'
		db.session.delete(user)
		db.session.commit()
		return 'User account has been deleted!'
	else:
		return 'Unsupported HTTP method!'

@app.route('/registerUser', methods=['POST'])
def register():
	if request.method == 'POST':
		if len(request.args) is 0:
			return 'Request was empty!'
		username = request.args['username']
		if not isProperUsername(username):
			return 'Invalid username!'
		password = request.args['password']
		if not isProperPassword(password):
			return 'Invalid password!'
		email = request.args['email']
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
			return 'Registration success!'
		return 'Registration failed!'
	else:
		return 'Unsupported HTTP method!'

# @app.route('/profile/<int:userid>', methods=['GET', 'POST', 'DELETE'])
# 	# if len(request.args) is 0:
# 	# 	return 'Request was empty!'

# @app.route('/createProfile', methods=['POST'])

# @app.route('/appointment/<int:apptid>', methods=['GET', 'POST', 'DELETE'])

# @app.route('/createAppt', method=['POST'])

# @app.route('/insurance/<int:insurid>', methods=['GET', 'POST', 'DELETE'])

# @app.route('/createInsurance', methods=['POST'])

if __name__ == '__main__':
	app.run(debug=True)