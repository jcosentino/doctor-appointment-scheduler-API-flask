from flask import Blueprint, request, jsonify
from db.models.user import User
from ..validation import isProperEmail

get_user_id = Blueprint('get_user_id', __name__)

@get_user_id.route('/getUserId', methods=['PUT'])
def getUserId():
	if request.method == 'PUT':
		input = request.get_json().get('input')
		if isProperEmail(input):
			user = User.query.filter_by(email=input).first()
		else:
			user = User.query.filter_by(username=input).first()
		if user is None:
			return jsonify('User does not exist!')
		return jsonify(userid=user.userid)
	return jsonify('Unsupported HTTP method!')