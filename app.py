from flask import Flask, redirect, url_for, render_template, request
from flask.ext.pymongo import PyMongo
from bson.json_util import dumps
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
import datetime
import json
import ast

"""
Flask for login/security issues, api
Angular for separate frontendy things
Four angular apps: 
	/app - analytics, dashboard
		analytics - view stats on menu usage
		dashboard - add menus, items, change prices, etc
	/menu - view actual menu (patron view)
	/ - landing page

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
	def __init__(self, username, password):
		self.username = username
		self.password = password

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
	return User(username, '')

@app.route('/login', methods=['GET','POST'])
def login():
	# remember=True
	login_user(User('carsons', 'testpass222', 'totallyemail@gmail.com'))
	return "logged in %s" % str(current_user.username)

@app.route("/logout")
@login_required
def logout():
	myUser = current_user.username
	logout_user()
	return 'logged out %s' % myUser

def userAsJson():
	# TODO: remove password field from this dictionary
    return json.dumps(current_user.__dict__.pop("password", None))

app.jinja_env.globals.update(userAsJson=userAsJson)

@app.route('/api/<restaurantName>/search/<query>')
def search(restaurantName, query):
	if query == 'blue cheese' and restaurantName == 'carsons':
		return app.send_static_file('test/carsonsbluecheese.json')
	else:
		return '"%s" not found for restaurant "%s"' % (query, restaurantName)

@app.route('/api/<restaurantName>')
def restaurantInfo(restaurantName):
	restaurantName = restaurantName.lower()
	return dumps(db.menus.find_one({"identifier": restaurantName}))

@app.route('/admin/resetdb')
@login_required
def resetDatabase():
	if current_user.username != 'carsons' and current_user.username != 'mitchellvitez':
		return 'Authentication failure', 403
	db.menus.remove({})
	with open ("static/test/carsons.json", "r") as myfile:
		data = myfile.read().replace('\n', '')
		db.menus.insert(ast.literal_eval(data))
	return "Success: reset database"

@app.route('/api/<restaurantName>/categories', methods=['GET', 'POST'])
def categories(restaurantName):
	restaurantName = restaurantName.lower()
	if request.method == 'POST':
		if current_user.username != restaurantName:
			return 'ERROR', 401 # TODO: better error data and error code handling
		else:
			request.data = ast.literal_eval(request.data)

			if request.data["action"] == "delete":
				db.menus.update({"identifier": restaurantName}, {"$pull": {"categories": request.data['category'] } })
			elif request.data["action"] == "save":
				db.menus.update({"identifier": restaurantName}, {"$push": {"categories": request.data['category'] } })

	return dumps(db.menus.find_one({"identifier": restaurantName}, {"categories.name": True}))

@app.route('/api/<restaurantName>/items', methods=['GET', 'POST'])
def items(restaurantName):
	restaurantName = restaurantName.lower()
	if request.method == 'POST':
		if current_user.username != restaurantName:
			return 'ERROR', 401
		else:
			request.data = ast.literal_eval(request.data)

			categoryName = request.data['item']['category']['name']
			try:
				del request.data['item']['category']
			except KeyError:
				pass # "category" should always be a key

			if request.data["action"] == "save":
				db.menus.update({"identifier": restaurantName, "categories.name": categoryName },
					{"$push" : {"categories.$.items" : request.data['item'] } } )
					
			# elif request.data["action"] == "delete":
			# 	db.menus.update({"identifier": restaurantName}, {"$pull": {"categories": request.data['category'] } })

	return dumps(db.menus.find_one({"identifier": restaurantName}, {"categories": True}))

@app.route('/api/<restaurantName>/style', methods=['GET', 'POST'])
def style(restaurantName):
	restaurantName = restaurantName.lower()
	if request.method == 'POST':
		if current_user.username != restaurantName:
			return 'ERROR', 401 # TODO: better error data and error code handling
		else:
			request.data = ast.literal_eval(request.data)

			# if request.data["action"] == "delete":
			# 	db.menus.update({"identifier": restaurantName}, {"$pull": {"style": request.data['element'] } })
			if request.data["action"] == "save":
				db.menus.update({"identifier": restaurantName}, {"$set": {"style": request.data['style'] } })

	return dumps(db.menus.find_one({"identifier": restaurantName}, {"style": True}))

# @app.route('/api/<restaurantName>/menus')
# def getMenus(restaurantName):
# 	restaurantName = restaurantName.lower()
# 	if restaurantName == 'carsons':
# 		return '["Main Menu", "Wine List", "Dessert Menu", "Breakfast Menu"]'
# 	else:
# 		return '[]'

@app.route('/manage')
@login_required
def manage():
	return render_template('manage.html')

@app.route('/menu/<restaurantName>')
def menu(restaurantName):
	return render_template('menu.html', restaurantName=restaurantName)

@app.route('/')
def home():
	return render_template('home.html')

if __name__ == '__main__':
	app.config['SECRET_KEY'] = 'TotallySecret2937498374982'
	app.run(debug=True)
