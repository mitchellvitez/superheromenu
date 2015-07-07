from flask import Flask, redirect, url_for, render_template, request
from flask.ext.pymongo import PyMongo
from bson.json_util import dumps
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
import datetime
import json
import ast
import bcrypt

"""
Flask for login/security issues, api
Angular for separate frontendy things
Four angular apps: 
	/app - analytics, dashboard
		analytics - view stats on menu usage
		dashboard - add menus, items, change prices, etc
	/menu - view actual menu (patron view)
	/ - landing page

from flask import Flask, redirect, url_for, render_template, request
app = Flask(__name__)
ctx = app.test_request_context()
ctx.push()

"""

app = Flask(__name__)
app.secret_key = 'TotallySecret2937498374982'


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
		db.users.update({'username': self.username, "password": self.password}, {"username": self.username, "password": self.password}, upsert=True)

	def is_authenticated(self):
		return db.users.find({'username': self.username, "password": self.password}).limit(1).count() > 0

	def is_active(self):
		return True # return db.users.find({'username': self.username, "password": self.password}).limit(1).count() > 0

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.username)

@login_manager.user_loader
def load_user(username, password=''):
	# returns user object, sans password, from this user id
	return User(username, password)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect("login")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/signup', methods=['GET','POST'])
def signup():
	if current_user.is_authenticated():
		return redirect('../manage')

	if request.method == 'POST':

		username = request.form['username']
		password = bcrypt.hashpw(request.form['password'], bcrypt.gensalt())
		email = request.form['email']

		rememberMe = request.form.get('remember')
		if rememberMe == 'true':
			rememberMe = True
		else:
			rememberMe = False

		if db.users.find( {'username': username } ).count() > 0:
			return redirect('login')

		if db.users.find( {'email': email } ).count() > 0:
			return redirect('login')

		if not username.isalnum():
			return render_template('signup.html')

		db.users.insert( {'username': username, "password": password, "email": email } )

		db.menus.insert( {'identifier': username,
			"style": {
				"general" : [
					{	"name": "Background Color",
					 	"value": "#ffffff"
					},
					{	"name": "Text Color",
						"value": "#444444"
					},
					{	"name": "Currency Symbol",
						"value": "$"
					},
					{	"name": "Font",
						"value": "'Hoefler Text', 'Baskerville Old Face', Garamond, 'Times New Roman', serif"
					},
				],
				"title": [
					{	"name": "Text Color",
						"value": "#444444"
					},
					{	"name": "Font",
						"value": "'Hoefler Text', 'Baskerville Old Face', Garamond, 'Times New Roman', serif"
					},
					{
						"name": "Font Size",
						"value": "300%"
					}
				],
				"category": [
					{	"name": "Header Text Color",
						"value": "#444444"
					},
					{
						"name": "Header Font",
						"value": "'Hoefler Text', 'Baskerville Old Face', Garamond, 'Times New Roman', serif"
					},
					{
						"name": "Header Font Size",
						"value": "220%"
					},
					{	"name": "Description Text Color",
						"value": "#444444"
					},
					{
						"name": "Description Font",
						"value": "'Hoefler Text', 'Baskerville Old Face', Garamond, 'Times New Roman', serif"
					},
					{
						"name": "Description Font Size",
						"value": "120%"
					}
				],
				"item": [
					{	"name": "Header Text Color",
						"value": "#444444"
					},
					{
						"name": "Header Font",
						"value": "'Hoefler Text', 'Baskerville Old Face', Garamond, 'Times New Roman', serif"
					},
					{
						"name": "Header Font Size",
						"value": "24px"
					},
					{	"name": "Description Text Color",
						"value": "#444444"
					},
					{
						"name": "Description Font",
						"value": "'Hoefler Text', 'Baskerville Old Face', Garamond, 'Times New Roman', serif"
					},
					{
						"name": "Description Font Size",
						"value": "120%"
					},
					{
						"name": "Description Style",
						"value": "italic"
					},
					{	"name": "Price Text Color",
						"value": "#444444"
					},
					{
						"name": "Price Font",
						"value": "'Hoefler Text', 'Baskerville Old Face', Garamond, 'Times New Roman', serif"
					},
					{
						"name": "Price Font Size",
						"value": "120%"
					},
				],
				"option": [
					{	
						"name": "Header Text Color",
						"value": "#444444"
					},
					{
						"name": "Header Font",
						"value": "'Hoefler Text', 'Baskerville Old Face', Garamond, 'Times New Roman', serif"
					},
					{
						"name": "Header Font Size",
						"value": "120%"
					},
					{	
						"name": "Price Text Color",
						"value": "#444444"
					},
					{
						"name": "Price Font",
						"value": "'Hoefler Text', 'Baskerville Old Face', Garamond, 'Times New Roman', serif"
					},
					{
						"name": "Price Font Size",
						"value": "120%"
					}
				],
				"info": [
					{	"name": "Header Text Color",
						"value": "#444444"
					},
					{
						"name": "Header Font",
						"value": "'Hoefler Text', 'Baskerville Old Face', Garamond, 'Times New Roman', serif"
					},
					{
						"name": "Header Font Size",
						"value": "20px"
					},
					{	"name": "Text Color",
						"value": "#444444"
					},
					{
						"name": "Font",
						"value": "'Hoefler Text', 'Baskerville Old Face', Garamond, 'Times New Roman', serif"
					},
					{
						"name": "Font Size",
						"value": "120%"
					}
				]
			},
			'name': username,
			'info' : [
					{
						"name": "Hours",
						"value": [
							{
								"name": "Monday-Friday",
								"value": "11am - 10pm"
							},
							{
								"name": "Weekends",
								"value": "Open 24 hours"
							},
						]
					},
					{
						"name": "Address",
						"value": [
							{
								"name": "Street Address",
								"value": "123 Great Restaurant Road",
							},
							{
								"name": "City",
								"value": "Menutown",
							},
							{
								"name": "Country",
								"value": "USA",
							},
						]
					},
					{
						"name": "Advisory",
						# "value": "Eat raw meat at your own risk"
						"value": [
							{
								"name": "Eat raw meat at your own risk",
								"value": ""
							}
						]
					}
				],
			'categories': [
					{	"name": "First Category",
						"description": "Menus are divided into categories of items. You can add and change categories and items in the manager.",
						"items": [
							{	"name": "Test Item",
								"description": "delicious, made with a house sauce and lots of love",
								"options": [
									{
										"name": "cup",
										"price": 4.50
									},
									{
										"name": "bowl",
										"price": 8
									}
								]
							},
							{	"name": "Item 2",
								"description": "You can also adjust the look and feel of your menu with \"Style\" in the manager",
								"price": 19.95
							}
						]
					},
					{	"name": "Appetizers",
						"description": "Yummy little pre-meal treats",
						"items": [
							{	"name": "Celery sticks",
								"description": "Like eating crunchy water",
								"price": 99
							}, 
						]
					}
				]
			})

		login_user(User(username, password), remember=rememberMe)
		if current_user.is_authenticated():
			return redirect('login')

	return render_template('signup.html')

@app.route('/motivation')
def motivation():
	return "<h1>MEDIOCRITY WILL NOT DO</h1>"

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		
		username = request.form['username']
		password = request.form['password']

		rememberMe = request.form.get('remember')
		if rememberMe == 'true':
			rememberMe = True
		else:
			rememberMe = False

		if db.users.find( {'username': username } ).count() > 0:
			userdata = db.users.find_one({'username': username}, {'_id': 0})
			userdata = ast.literal_eval(str(userdata))

			if bcrypt.checkpw(password, userdata['password']):
				login_user(User(username, password), remember=rememberMe)

	if current_user.is_authenticated():
		return redirect('../manage')

	return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect('/')


def userAsJson():
    return json.dumps(current_user.__dict__) #.pop("password", None))

app.jinja_env.globals.update(userAsJson=userAsJson)


@app.route('/api/<restaurantName>/filter/<query>')
def filter(restaurantName, query):

	# only deal with lowercase
	query = query.lower().split(' ')
	menu = ast.literal_eval(dumps( db.menus.find_one({"identifier": restaurantName}, {"categories": True}) ).lower())

	result = {"categories": [], "items": []}

	print query

	for category in menu['categories']:
		for item in category['items']:
			for word in query:
				if word in item['name'] or word in item.get('description', ''):
					result['items'].append(item)

	return dumps(result)


@app.route('/api/<restaurantName>/search/<query>')
def search(restaurantName, query):

	# only deal with lowercase
	query = query.lower().split(' ')
	menu = ast.literal_eval(dumps( db.menus.find_one({"identifier": restaurantName}, {"categories": True}) ))

	result = {"categories": [], "items": []}

	for category in menu['categories']:
		for word in query:
			if word in category['name'].lower() or word in category.get('description', '').lower():
				result['categories'].append(category)

	for category in menu['categories']:
		for item in category['items']:
			for word in query:
				if word in item['name'].lower() or word in item.get('description', '').lower():
					result['items'].append(item)

	return dumps(result)

@app.route('/api/<restaurantName>')
def restaurantInfo(restaurantName):
	restaurantName = restaurantName.lower()
	return dumps(db.menus.find_one({"identifier": restaurantName}))

@app.route('/admin/resetdb')
#@login_required
def resetDatabase():
	#if current_user.username != 'carsons' and current_user.username != 'mitchellvitez':
		#return 'Authentication failure', 403
	db.menus.remove({})
	db.users.remove({})
	with open ("static/test/carsons.json", "r") as myfile:
		data = myfile.read().replace('\n', '')
		db.menus.insert(ast.literal_eval(data))
	return "Success: reset database"

@app.route('/api/<restaurantName>/info', methods=['GET', 'POST'])
def info(restaurantName):
	restaurantName = restaurantName.lower()
	if request.method == 'POST':
		if current_user.username != restaurantName:
			return 'ERROR', 401
		else:
			print request.data
			request.data = ast.literal_eval(request.data)

			# if request.data["action"] == "delete":
			# 	db.menus.update({"identifier": restaurantName}, {"$pull": {"info": request.data['info'] } })
			if request.data["action"] == "save":
				db.menus.update({"identifier": restaurantName}, {"$set": {"info": request.data['info']['info'] } })

	return dumps(db.menus.find_one({"identifier": restaurantName}, {"info": True}))

@app.route('/api/<restaurantName>/categories', methods=['GET', 'POST'])
def categories(restaurantName):
	restaurantName = restaurantName.lower()
	if request.method == 'POST':
		if current_user.username != restaurantName:
			return 'ERROR', 401
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

			elif request.data["action"] == "update":

				originalCategoryName = request.data['originalItem']['category']['name']
				try:
					del request.data['originalItem']['category']
				except KeyError:
					pass # "category" should always be a key

				db.menus.update({"identifier": restaurantName, "categories.name": originalCategoryName },
					{"$pull" : {"categories.$.items" : request.data['originalItem'] } } )
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
			return 'ERROR', 401
		else:
			request.data = ast.literal_eval(request.data)

			# if request.data["action"] == "delete":
			# 	db.menus.update({"identifier": restaurantName}, {"$pull": {"style": request.data['element'] } })
			if request.data["action"] == "save":
				styleAndComponent = "style." + request.data["component"]

				print styleAndComponent
				print request.data

				db.menus.update({"identifier": restaurantName}, {"$set": {styleAndComponent: request.data['style'] } })

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
	return render_template('manage.html', username=current_user.username, restaurantName=current_user.username)

@app.route('/discuss')
# @login_required
def discuss():
	return render_template('discuss.html')

@app.route('/view/<restaurantName>')
@app.route('/menu/<restaurantName>')
def menu(restaurantName):
	return render_template('menu.html', restaurantName=restaurantName)

@app.route('/')
def home():
	return render_template('home.html')

if __name__ == '__main__':
	app.secret_key = 'TotallySecret2937498374982'
	app.config['SECRET_KEY'] = 'TotallySecret2937498374982'
	app.run(debug=True)
