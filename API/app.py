#Need to modularize the Flask logic
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
#create_sql =  './Files/create.sql'

app = Flask(__name__)
CORS(app) #Need for access from other applications, such as Axios
#Should create schema if it doesn't already exist
#unsure how to do this
#
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:8milerun@localhost/testdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Turn off annoying message
db = SQLAlchemy(app)

#DateTime in flask-sqlalchemy is Python datetime. Conversion to MySQL might be necessary
class User(db.Model):
	userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(80), unique=False, nullable=False)
	password = db.Column(db.String(16), unique=False, nullable=False)
	email = db.Column(db.String(80), unique=False, nullable=False)
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
	insuranceid = db.Column(db.Integer, db.ForeignKey('insurance.insuranceid'), nullable=False)
	insurancecompany = db.relationship('Insurace', backref='Profile', lazy=True)
	groupnumber = db.relationship('Insurace', backref='Profile', lazy=True)
	memberid = db.relationship('Insurace', backref='Profile', lazy=True)

class Appointment(db.Model):
	appointmentid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	apptTime = db.Column(db.DateTime, nullable=True)
	available = db.Column(db.Boolean, nullable=False, default=True)
	'''
	month
	day
	year
	time
	amOrPm
	'''
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

@app.route('/user/<user_id>', methods=['GET, POST, DELETE'])
def user(user_id):
	if request.method == 'GET':
		#return data
		print(user_id)
	# else if request.method == 'POST':
	# 	#modify
	# elif request.method == 'DELETE':
	# 	#delete
	# else:
	# 	#Error 405 Method Not Allowed

if __name__ == '__main__':
	app.run(debug=True)