from flask import Blueprint, request, jsonify
from db.global_db import db
from db.models.user import User

toggle_admin = Blueprint('toggle_admin', __name__)

@toggle_admin.route('/toggleAdmin/<int:userid>', methods=['PATCH'])
def toggleAdmin(userid):
	if request.method == 'PATCH':
		user = User.query.filter_by(userid=userid).first()
		print(user.isadmin)
		user.isadmin = True if user.isadmin is False else False
		db.session.commit()
		return jsonify('User\'s administrative privileges have been changed!')

