from flask import Blueprint, request, jsonify
from db.models.insurance import Insurance
from datetime import datetime

find_insr = Blueprint('find_insr', __name__)

@find_insr.route('/findInsurance', methods=['PUT'])
def findInsurance():
	if request.method == 'PUT':
		data = request.form
		insurance = Insurance.query.filter_by(insurancecompany=data['insurancecompany']).first()
		if insurance is None:
			return 'That insurance company does not exist!'
		return jsonify(insuranceid=insurance.insuranceid)
	return 'Unsupported HTTP method!'