from flask import Blueprint, request, jsonify
from db.global_db import db
from db.models.appointment import Appointment
from datetime import datetime

create_appt = Blueprint('create_appt', __name__)

@create_appt.route('/createAppt', methods=['POST'])
def createAppt():
	if request.method == 'POST':
		data = request.get_json()
		if len(data) is 0:
			return jsonify('Request was empty!')
		apptTime = data.get('apptTime')
		appointment = Appointment.query.filter_by(apptTime=apptTime).first()
		if appointment is not None:
			return jsonify('Cannot make an appointment at that time!')
		createdDate = datetime.now()
		lastUpdated = datetime.now()
		appointment = Appointment(apptTime=apptTime,
								  createdDate=createdDate, lastUpdated=lastUpdated)
		db.session.add(appointment)
		db.session.commit()
		return jsonify('Registration success!')
