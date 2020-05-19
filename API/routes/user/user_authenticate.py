from flask import Blueprint, request, jsonify
from db.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from ..validation import isProperEmail

user_authenticate = Blueprint('user_authenticate', __name__)

@user_authenticate.route('/authenticate', methods=['POST'])
def authenticate():
	if request.method == 'POST':
		data = request.get_json()
		email = data.get('email')
		user = User.query.filter_by(email=email).first()
		password = data.get('password')
		if user is None or (check_password_hash(user.password, password) is False):
			return jsonify('Authentication failed!')
		return jsonify('Authentication succeeded!')
