from flask import Blueprint, request, jsonify
from db.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from ..validation import isProperEmail

user_authenticate = Blueprint('user_authenticate', __name__)

@user_authenticate.route('/authenticate', methods=['POST'])
def authenticate():
	if request.method == 'POST':
		data = request.get_json()
		username = data.get('username')
		if isProperEmail(username):
			user = User.query.filter_by(email=username).first()
		else:
			user = User.query.filter_by(username=username).first()
		password = data.get('password')
		if user is None or (check_password_hash(user.password, password) is False):
			return jsonify('Authentication failed!')
		return jsonify('Authentication succeeded!')
