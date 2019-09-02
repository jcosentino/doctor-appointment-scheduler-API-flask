from flask import Blueprint, request
from db.global_db import db
from db.models.appointment import Appointment
from db.models.profile import Profile

cancel_appt = Blueprint('cancel_appt', __name__)

@cancel_appt.route('/cancelAppointment/<int:userid>', methods=['PUT'])
def cancelAppointment(userid):
	if request.method == 'PUT':
		data = request.form
		appointmentid = data['appointmentid']
		appointment = Appointment.query.filter_by(appointmentid=appointmentid).first()
		if appointment.available is True:
			return 'That appointment is already available.'
		appointment.available = True
		profile = Profile.query.filter_by(userid=userid).first()
		profile.appointmentid = None
		db.session.commit()
		return 'Appointment canceled!'
	return 'Unsupported HTTP method!'