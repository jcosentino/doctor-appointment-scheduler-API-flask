from flask import Blueprint, request, jsonify
from db.global_db import db
from db.models.appointment import Appointment
from db.models.profile import Profile

cancel_appt = Blueprint('cancel_appt', __name__)

@cancel_appt.route('/cancelAppointment/<int:userid>', methods=['PATCH'])
def cancelAppointment(userid):
	if request.method == 'PATCH':
		data = request.get_json()
		appointmentid = data.get('appointmentid')
		appointment = Appointment.query.filter_by(appointmentid=appointmentid).first()
		if appointment.available is True:
			return jsonify('That appointment is already available.')
		appointment.available = True
		profile = Profile.query.filter_by(userid=userid).first()
		profile.appointmentid = None
		db.session.commit()
		return jsonify('Appointment canceled!')
	return jsonify('Unsupported HTTP method!')