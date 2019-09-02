from ..global_db import db
from datetime import datetime

class Appointment(db.Model):
	appointmentid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	apptTime = db.Column(db.DateTime, unique=True, nullable=True)
	available = db.Column(db.Boolean, nullable=False, default=True)
	createdDate = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	lastUpdated = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)