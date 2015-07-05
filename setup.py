import os

os.system('git pull')

s = ''

with open("app.py", "rt") as fin:
	for line in fin:
		s += line
            
with open("app.py", "wt") as fout:
	fout.write(s.replace('app.run(debug=True)', 'app.run()').replace("@app.route('/admin/resetdb')", "# @app.route('/admin/resetdb')"))
