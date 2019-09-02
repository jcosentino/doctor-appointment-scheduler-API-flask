from ..global_db import db
from datetime import datetime

class User(db.Model):
	userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(16), unique=True, nullable=False)
	password = db.Column(db.String(512), unique=False, nullable=False)
	email = db.Column(db.String(80), unique=True, nullable=False)
	createdDate = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	lastUpdated = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	isadmin = db.Column(db.Boolean, nullable=False, default=False)