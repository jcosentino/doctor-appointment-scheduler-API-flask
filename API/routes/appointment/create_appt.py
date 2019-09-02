from flask import Blueprint, request
from db.global_db import db
from db.models.appointment import Appointment
from datetime import datetime

create_appt = Blueprint('create_appt', __name__)

@create_appt.route('/createAppt', methods=['POST'])
def createAppt():
	if request.method == 'POST':
		data = request.form
		if len(data) is 0:
			return 'Request was empty!'
		apptTime = data['apptTime']
		appointment = Appointment.query.filter_by(apptTime=apptTime).first()
		if appointment is not None:
			return 'Cannot make an appointment at that time!'
		createdDate = datetime.now()
		lastUpdated = datetime.now()
		appointment = Appointment(apptTime=apptTime,
								  createdDate=createdDate, lastUpdated=lastUpdated)
		db.session.add(appointment)
		db.session.commit()
		return 'Registration success!'
	else:
		return 'Unsupported HTTP method!'