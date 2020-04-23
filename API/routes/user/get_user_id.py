from flask import Blueprint, request, jsonify
from db.models.user import User

get_user_id = Blueprint('get_user_id', __name__)

@get_user_id.route('/getUserId/<username>', methods=['GET'])
def getUserId(username):
	if request.method == 'GET':
		user = User.query.filter_by(username=username).first()
		if user is None:
			return 'User does not exist!'
		return jsonify(userid=user.userid)
	return jsonify('Unsupported HTTP method!')