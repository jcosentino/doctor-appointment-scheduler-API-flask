from ..global_db import db
from datetime import datetime

class Insurance(db.Model):
	insuranceid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	insurancecompany = db.Column(db.String(80), unique=True, nullable=False)
	groupnumber = db.Column(db.String(16), nullable=False)
	memberid = db.Column(db.String(16), unique=False, nullable=False)
	createdDate = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	lastUpdated = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)