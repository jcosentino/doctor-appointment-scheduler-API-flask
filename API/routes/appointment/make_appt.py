from flask import Blueprint, request, jsonify
from db.global_db import db
from db.models.appointment import Appointment
from db.models.profile import Profile

make_appt = Blueprint('make_appt', __name__)

@make_appt.route('/makeAppointment/<int:userid>', methods=['PATCH'])
def makeAppointment(userid):
	if request.method == 'PATCH':
		data = request.get_json()
		appointmentid = data.get('appointmentid')
		appointment = Appointment.query.filter_by(appointmentid=appointmentid).first()
		if appointment.available is False:
			return jsonify('That apointment is not available!')
		appointment.available = False
		profile = Profile.query.filter_by(userid=userid).first()
		profile.appointmentid = appointmentid
		db.session.commit()
		return jsonify('Appointment successfully booked.')
	return jsonify('Unsupported HTTP method!')
