from flask import Flask
from flask_cors import CORS
from db.schema.schema_creation import check_schema
from db.schema.db_connection import initConnections
from db.global_db import db
import argparse

#Routes
from routes.user.user_func import user_func
from routes.user.user_registration import user_registration
from routes.user.user_authenticate import user_authenticate
from routes.user.toggle_admin import toggle_admin
from routes.user.get_user_id import get_user_id
from routes.user.security_question import security_question
from routes.profile.profile_func import profile_func
from routes.appointment.appointment_func import appointment_func
from routes.appointment.create_appt import create_appt
from routes.appointment.make_appt import make_appt
from routes.appointment.cancel_appt import cancel_appt
from routes.appointment.find_appt import find_appt
from routes.insurance.insurance_func import insurance_func
from routes.insurance.create_insr import create_insr
from routes.insurance.register_insr import register_insr
from routes.insurance.deregister_insr import deregister_insr
from routes.insurance.find_insr import find_insr

# cli variables
parser = argparse.ArgumentParser()
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--hostname')
parser.add_argument('--schema_name')
args = parser.parse_args()
username = args.username
password = args.password
hostname = args.hostname
schema_name = args.schema_name
var_args = [username, password, hostname, schema_name]

app = Flask(__name__)
#Need for access from other applications, such as Axios
CORS(app, resources={r"/*": {"origins": "*"}})

#Check if the schema exists and create it if needed
check_schema(*var_args)

#Configure app for testdb connection
initConnections(app, *var_args)

#Create database tables
db.init_app(app)
with app.app_context():
	db.create_all()

#Register all routes for usage
app.register_blueprint(user_func)
app.register_blueprint(user_registration)
app.register_blueprint(user_authenticate)
app.register_blueprint(toggle_admin)
app.register_blueprint(get_user_id)
app.register_blueprint(security_question)
app.register_blueprint(profile_func)
app.register_blueprint(appointment_func)
app.register_blueprint(create_appt)
app.register_blueprint(make_appt)
app.register_blueprint(cancel_appt)
app.register_blueprint(find_appt)
app.register_blueprint(insurance_func)
app.register_blueprint(create_insr)
app.register_blueprint(register_insr)
app.register_blueprint(deregister_insr)
app.register_blueprint(find_insr)

if __name__ == '__main__':
	app.run()