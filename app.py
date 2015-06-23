from flask import Flask
app = Flask(__name__)

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
