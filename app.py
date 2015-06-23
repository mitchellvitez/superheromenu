from flask import Flask, redirect, url_for
from flask.ext.pymongo import PyMongo
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
import datetime

"""
Flask for login/security issues, api
Angular for separate frontendy things
"""

app = Flask(__name__)

# set up database
mongo = PyMongo(app)
with app.app_context():
	db = mongo.db

# set up user logins
login_manager = LoginManager()
login_manager.init_app(app)

class User():
	def __init__(self, username, password, email):
		self.username = username
		self.password = password
		self.email = email

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.username)

@login_manager.user_loader
def load_user(username):
	# returns user object, sans password, from this user id
	# return db.users.find_one({'username': username}, {'password': False})
	return User('mitchellvitez', 'testpass', 'mitchellvitez@gmail.com')

@app.route('/login',methods=['GET','POST'])
def login():
	login_user(User('mitchellvitez', 'testpass', 'mitchellvitez@gmail.com'))
	return "logged in %s" % str(current_user.username)

@app.route("/logout")
@login_required
def logout():
	myUser = current_user.username
	logout_user()
	return 'logged out %s' % myUser

@app.route('/testdb')
@login_required
def testDatabase():
	# db.users.remove() # remove all users
	# db.users.save({'username':'mitchellvitez', 'online':True})
	# return str( mongo.db.users.find_one() )
	return 'users: %s' % db.users.find_one()

@app.route('/api/<restaurantName>/search/<query>')
def search(restaurantName, query):
	if query == 'blue cheese' and restaurantName == 'carsons':
		return app.send_static_file('test/carsonsbluecheese.json')
	else:
		return '"%s" not found for restaurant "%s"' % (query, restaurantName)

@app.route('/api/<restaurantName>')
def restaurantInfo(restaurantName):
	restaurantName = restaurantName.lower()
	if restaurantName == 'carsons':
		return app.send_static_file('test/carsons.json')
	else:
		return 'No such restaurant'

@app.route('/create')
@login_required
def create():
	return "Menu creation screen here"

@app.route('/analytics')
@login_required
def analytics():
	return "Analytics screen here"

@app.route('/menu/<restaurantName>')
def menu(restaurantName):
	return "Menu for %s that goes in iframe here" % restaurantName

@app.route('/')
def landingPage():
	return "Landing page here"

if __name__ == '__main__':
	app.config['SECRET_KEY'] = 'TotallySecret2937498374982'
	app.run(debug=True)
