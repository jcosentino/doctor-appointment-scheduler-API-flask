from flask import Blueprint, request
from db.global_db import db
from db.models.insurance import Insurance
from db.models.profile import Profile

register_insr = Blueprint('register_insr', __name__)

@register_insr.route('/registerInsurance/<int:userid>', methods=['PATCH'])
def registerInsurance(userid):
	if request.method == 'PATCH':
		data = request.form
		insuranceid = data['insuranceid']
		profile = Profile.query.filter_by(userid=userid).first()
		if str(profile.insuranceid) == insuranceid:
			return 'That insurance company is already registered to that user!'
		profile.insuranceid = insuranceid
		db.session.commit()
		return 'Insurance successfully applied.'
	return 'Unsupported HTTP method!'