from flask import Blueprint, request, jsonify
from db.global_db import db
from db.models.insurance import Insurance
from ..validation import isValidGroupNumber, isValidMemberid
from datetime import datetime

create_insr = Blueprint('create_insr', __name__)

@create_insr.route('/createInsurance', methods=['POST'])
def createInsurance():
	if request.method == 'POST':
		data = request.get_json()
		if len(data) is 0:
			return jsonify('Request was empty!')
		insurancecompany = data.get('insurancecompany')
		groupnumber = data.get('groupnumber')
		if not isValidGroupNumber(groupnumber):
			return jsonify('Invalid Group Number!')
		memberid = data.get('memberid')
		if not isValidMemberid(memberid):
			return jsonify('Invalid Member ID!')
		createdDate = datetime.now()
		lastUpdated = datetime.now()
		insurance = Insurance(insurancecompany=insurancecompany, groupnumber=groupnumber,
							  memberid=memberid, createdDate=createdDate, lastUpdated=lastUpdated)
		db.session.add(insurance)
		db.session.commit()
		return jsonify('Registration success!')
	else:
		return jsonify('Unsupported HTTP method!')