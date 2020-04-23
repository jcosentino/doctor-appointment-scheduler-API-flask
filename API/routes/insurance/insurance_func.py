from flask import Blueprint, request, jsonify
from db.global_db import db
from db.models.insurance import Insurance
from db.models.profile import Profile
from datetime import datetime

insurance_func = Blueprint('insurance_func', __name__)

@insurance_func.route('/insurance/<int:insuranceid>', methods=['GET', 'POST', 'DELETE'])
def insurance(insuranceid):
	if request.method == 'GET':
		insurance = Insurance.query.filter_by(insuranceid=insuranceid).first()
		if insurance is None: #if query is empty
			return jsonify('None')
		insuranceid = insurance.insuranceid
		insurancecompany = insurance.insurancecompany
		groupnumber = insurance.groupnumber
		memberid = insurance.memberid
		createdDate = insurance.createdDate
		lastUpdated = insurance.lastUpdated
		obj = jsonify(insuranceid=insuranceid, insurancecompany=insurancecompany, 
					  groupnumber=groupnumber, memberid=memberid, 
					  createdDate=createdDate, lastUpdated=lastUpdated)
		return obj
	elif request.method == 'POST':
		data = request.get_json()
		insurance = Insurance.query.filter_by(insuranceid=insuranceid).first()
		if insurance is None: #if query is empty
			return jsonify('Cannot update that insurance company! It does not exist!')
		insurancecompany = insurance.insurancecompany if data.get('insurancecompany') is None \
			else data['insurancecompany']		
		groupnumber = insurance.groupnumber if data.get('groupnumber') is None \
			else data['groupnumber']	
		memberid = insurance.memberid if data.get('memberid') is None \
			else data['memberid']
		insurance.insurancecompany = insurancecompany
		insurance.groupnumber = groupnumber
		insurance.memberid = memberid
		insurance.lastUpdated = datetime.now()
		db.session.commit()
		return jsonify('Insurance has been updated!')
	elif request.method == 'DELETE':
		insurance = Insurance.query.filter_by(insuranceid=insuranceid).first()
		if insurance is None: #if query is empty
			return jsonify('Cannot delete that insurance company! It does not exist!')
		#Remove insuranceid from all user profiles
		profile = Profile.query.filter_by(insuranceid=insuranceid).all()
		if profile is not None:
			for p in profile:
				p.insuranceid = None
		db.session.delete(insurance)
		db.session.commit()
		return jsonify('Insurance has been deleted!')
	else:
		return jsonify('Unsupported HTTP method!')