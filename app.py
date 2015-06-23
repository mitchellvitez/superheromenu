from flask import Flask
app = Flask(__name__)

@app.route('/api/carsons/search/<query>')
def search(query):
	print query
	if query == "blue cheese":
		return app.send_static_file('test/carsonsbluecheese.json')
	else:
		return query + " end"

@app.route('/api/<restaurantName>')
def restaurantInfo(restaurantName):
	restaurantName = restaurantName.lower()
	if restaurantName == "carsons":
		return app.send_static_file('test/carsons.json')
	else:
		return "No such restaurant"

if __name__ == '__main__':
	app.run(debug=True)
