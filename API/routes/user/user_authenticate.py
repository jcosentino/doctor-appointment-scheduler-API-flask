from flask import Blueprint, request
from db.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

user_authenticate = Blueprint('user_authenticate', __name__)

@user_authenticate.route('/authenticate', methods=['POST'])
def authenticate():
	if request.method == 'POST':
		data = request.get_json()
		username = data.get('username')
		password = data.get('password')
		user = User.query.filter_by(username=username).first()
		if user is None:
			return 'User does not exist!'
		if (username != user.username) or \
		   (check_password_hash(user.password, password) is False):
		   return 'Authentication failed!'
		return 'Authentication succeeded!'
	return 'Unsupported HTTP method!'