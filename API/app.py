#Need to modularize the Flask logic
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:8milerun@localhost/testdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Turn off annoying message
db = SQLAlchemy(app)

#Should create schema if it doesn't already exist
#

class Person(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(80), unique=False, nullable=False)

@app.route('/')
def hello():
	print('Hello world!')
	return 'Hello world!'

@app.route('/nothing')
def handleNothing():
	return 'Nothing!'

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
	if request.method == 'POST':
		json_data = request.get_json()
		addData = Person(name=json_data)
		db.session.add(addData)
		db.session.commit()

if __name__ == '__main__':
	app.run()