from flask import Blueprint, request, jsonify
from db.global_db import db
from db.models.user import User
from db.models.profile import Profile
from db.models.appointment import Appointment
from db.models.insurance import Insurance
from ..validation import isValidSsn, isValidPhonenumber
from datetime import datetime

profile_func = Blueprint('profiprofile_funcle', __name__)

@profile_func.route('/profile/<int:userid>', methods=['GET', 'PUT'])
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
		obj = jsonify(profileid=profileid, firstname=firstname, 
					  lastname=lastname, ssn=ssn, phonenumber=phonenumber, 
					  birthdate=birthdate, createdDate=createdDate, 
					  lastUpdated=lastUpdated, userid=userid,
					  insuranceid=insuranceid, appointmentid=appointmentid)
		return obj
	elif request.method == 'PUT':
		data = request.form
		profile = Profile.query.filter_by(userid=userid).first()
		if profile is None: #if query is empty
			return 'Cannot update that profile! It does not exist!'
		firstname = profile.firstname if data.get('firstname') is None \
				or data['firstname'] is "" \
				else data['firstname']		
		lastname = profile.lastname if data.get('lastname') is None \
				or data['lastname'] is "" \
				else data['lastname']	
		ssn = profile.ssn if data.get('ssn') is None \
				or data['ssn'] is "" \
				else data['ssn']	
		if not isValidSsn(ssn):
			return 'Invalid SSN!'
		phonenumber = profile.phonenumber if data.get('phonenumber') is None \
				or data['phonenumber'] is "" \
				else data['phonenumber']
		if not isValidPhonenumber(phonenumber):
			return 'Invalid phone number!'
		birthdate = profile.birthdate if data.get('birthdate') is None \
				or data['birthdate'] is "" \
				else data['birthdate']
		if data.get('insuranceid') is not None:
			insuranceid = data['insuranceid']
			if Insurance.query.filter_by(insuranceid=insuranceid).first() is None:
				return 'No insurances exist with that insuranceid!'
			profile.insuranceid = insuranceid
		if data.get('appointmentid') is not None:
			appointmentid = data['appointmentid']
			appointment = Appointment.query.filter_by(appointmentid=appointmentid).first()
			if appointment is None:
				return 'No appointments exist with that appointmentid!'
			availability = appointment.available
			if availability is False:
				appointmentid = profile.appointmentid
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