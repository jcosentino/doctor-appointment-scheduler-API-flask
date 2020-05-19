from flask import Blueprint, request, jsonify
from db.global_db import db
from db.models.appointment import Appointment
from db.models.profile import Profile
from ..validation import checkAvailable
from datetime import datetime

appointment_func = Blueprint('appointment_func', __name__)

@appointment_func.route('/appointment/<int:appointmentid>', methods=['GET', 'PUT', 'DELETE'])
def appointment(appointmentid):
	if request.method == 'GET':
		appointment = Appointment.query.filter_by(appointmentid=appointmentid).first()
		if appointment is None: #if query is empty
			return jsonify('None')
		appointmentid = appointment.appointmentid
		apptTime = appointment.apptTime
		available = appointment.available
		createdDate = appointment.createdDate
		lastUpdated = appointment.lastUpdated
		obj = jsonify(appointmentid=appointmentid, apptTime=apptTime, 
					  available=available, createdDate=createdDate, 
					  lastUpdated=lastUpdated)
		return obj
	elif request.method == 'PUT':
		data = request.get_json()
		appointment = Appointment.query.filter_by(appointmentid=appointmentid).first()
		if appointment is None: #if query is empty
			return jsonify('Cannot update that appointment! It does not exist!')
		apptTime = appointment.apptTime if data.get('apptTime') is None \
			else data.get('apptTime') # YYYY-MM-DD HH:MM:SS
		available = appointment.available if data.get('available') is None \
			else data.get('available') # Needs to be 1 for True, 0 for False
		if not checkAvailable(available):
			return jsonify('Wrong format for availability')
		available = False if available is '0' else True
		appointment.apptTime = apptTime
		appointment.available = available
		if appointment.available is False:
			profile = Profile.query.filter_by(appointmentid=appointmentid).first()
			if profile is not None:
				profile.appointmentid = None
		appointment.lastUpdated = datetime.now()
		db.session.commit()
		return jsonify('Appointment has been updated!')
	elif request.method == 'DELETE':
		appointment = Appointment.query.filter_by(appointmentid=appointmentid).first()
		if appointment is None: #if query is empty
			return jsonify('Cannot delete that appointment! It does not exist!')
		#Remove appointmentid from user profiles
		profile = Profile.query.filter_by(appointmentid=appointmentid).first()
		if profile is not None:
			profile.appointmentid = None
		db.session.delete(appointment)
		db.session.commit()
		return jsonify('Appointment has been deleted!')
