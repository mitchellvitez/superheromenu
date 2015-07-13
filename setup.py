import os

os.system('git stash')
os.system('git pull')

s = ''

with open("app.py", "rt") as fin:
	for line in fin:
		s += line
            
with open("app.py", "wt") as fout:
	s = s.replace('app.run(debug=True)', 'app.run()')
	s = s.replace("@app.route('/admin/resetdb')", "# @app.route('/admin/resetdb')")
	fout.write(s)
