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
	return User(username, '', 'totallyemail@gmail.com')

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
    return json.dumps(current_user.__dict__)

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
			return 'ERROR', 401
		else:
			print "Request data: ", request.data

			request.data = ast.literal_eval(request.data)

			if request.data["action"] == "delete":
				print "ACTION IS DELETE"
				db.menus.update({"identifier": restaurantName}, {"$pull": {"categories": request.data['category'] } })
			
			elif request.data["action"] == "push":
				print "ACTION IS PUSH"
				db.menus.update({"identifier": restaurantName}, {"$push": {"categories": request.data['category'] } })

				"""
				categoryNum = request.data.count('"name"')
				s = request.data.replace('{', '').replace('}', '').replace('[', '{').replace(']', '}')

				for i in range(categoryNum):
					# s = s.replace('"name"', '"categories.%d.name"' % i, 1)
					s = s.replace('"name"', '"categories.$.name"')
					# s = s.replace(',,', ',')
				print s

				categoriesAsDict = ast.literal_eval(s)
				resultDict = {}
				deleteDict = {}
				for key, value in categoriesAsDict.items():
					if value not in resultDict.values():
						resultDict[key] = value
					else:
						deleteDict[key] = value

				print '====='
				print resultDict
				print deleteDict

				# if len(deleteDict) > 0:
				# 	db.menus.update({"identifier": restaurantName}, { "$set": resultDict, "$unset": deleteDict })
				# else:
				db.menus.update({"identifier": restaurantName}, { "$set": resultDict })
				"""

	return dumps(db.menus.find_one({"identifier": restaurantName}, {"categories.name": True}))

@app.route('/api/<restaurantName>/items', methods=['GET', 'POST'])
def items(restaurantName):
	restaurantName = restaurantName.lower()
	if request.method == 'POST':
		if current_user.username != restaurantName:
			return 'ERROR', 401
		else:
			# put data in db
			return '[]';
	return dumps(db.menus.find_one({"identifier": restaurantName}, {"categories": True}))

@app.route('/api/<restaurantName>/menus')
def getMenus(restaurantName):
	restaurantName = restaurantName.lower()
	if restaurantName == 'carsons':
		return '["Main Menu", "Wine List", "Dessert Menu", "Breakfast Menu"]';
	else:
		return '[]';

# @app.route('/api/<restaurantName>/insert')

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
