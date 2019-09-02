from ..global_db import db
from datetime import datetime

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