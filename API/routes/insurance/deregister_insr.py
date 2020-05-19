from flask import Blueprint, request, jsonify
from db.global_db import db
from db.models.insurance import Insurance
from db.models.profile import Profile

deregister_insr = Blueprint('deregister_insr', __name__)

@deregister_insr.route('/deregisterInsurance/<int:userid>', methods=['PATCH'])
def deregisterInsurance(userid):
	if request.method == 'PATCH':
		profile = Profile.query.filter_by(userid=userid).first()
		if profile.insuranceid is None:
			return jsonify('This user profile does not have any insurance!')
		profile.insuranceid = None
		db.session.commit()
		return jsonify('Insurance successfully deregistered!')
