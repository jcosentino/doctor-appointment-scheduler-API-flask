from flask import Blueprint, request, jsonify
from db.global_db import db
from db.models.appointment import Appointment

find_appt = Blueprint('find_appt', __name__)

@find_appt.route('/findAppointment', methods=['PUT'])
def findAppointment():
	if request.method == 'PUT':
		data = request.get_json()
		appointment = Appointment.query.filter_by(apptTime=data.get('apptTime')).first()
		if appointment is None:
			return 'That appointment does not exist!'
		return jsonify(appointmentid=appointment.appointmentid)
	return 'Unsupported HTTP method!'