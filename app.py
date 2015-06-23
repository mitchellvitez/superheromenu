from flask import Flask
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)

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
	app.run(debug=True)
