from flask import Flask, redirect, url_for
from flask.ext.pymongo import PyMongo
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user

"""
Flask for login/security issues, api
Angular for separate frontendy things
"""

app = Flask(__name__)

# set up database
mongo = PyMongo(app)

# set up user logins
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
	return mongo.db.users.find_one({'username': username})

@app.route('/login',methods=['GET','POST'])
def login():
    return "redirect(url_for('index'))"

@app.route('/testdb')
def testDatabase():
	mongo.db.users.remove() # remove all users
	mongo.db.users.save({'username':'mitchellvitez', 'online':True})
	# return str( mongo.db.users.find_one() )
	return 'users online: %s' % mongo.db.users.find_one({'online': True})

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
