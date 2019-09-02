from flask import Blueprint, request
from db.global_db import db
from db.models.appointment import Appointment
from db.models.profile import Profile

make_appt = Blueprint('make_appt', __name__)

@make_appt.route('/makeAppointment/<int:userid>', methods=['PUT'])
def makeAppointment(userid):
	if request.method == 'PUT':
		data = request.form
		appointmentid = data['appointmentid']
		appointment = Appointment.query.filter_by(appointmentid=appointmentid).first()
		if appointment.available is False:
			return 'That apointment is not available!'
		appointment.available = False
		profile = Profile.query.filter_by(userid=userid).first()
		profile.appointmentid = appointmentid
		db.session.commit()
		return 'Appointment successfully booked.'
	return 'Unsupported HTTP method!'
