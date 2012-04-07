import flask, json
from flask import Flask, g, render_template, request, session, redirect, url_for
import itertools
import re
import os

import models

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!j4mNLWX/,?RT'
db = models.init(os.environ.get("DATABASE_URL", "sqlite:///development.sqlite3"))

@app.before_request
def before_request():
	g.db = db()

@app.teardown_request
def teardown_request(exception=None):
	if hasattr(g, 'db'):
		g.db.close()

@app.route("/courses")
def courses():
	match_with = request.args.get('term', None)
	if not match_with:
	    return json.dumps([])
	matches = g.db.query(models.Course).filter(
	    models.Course.name.like('%' + match_with + '%')).all()
	print matches
	course_data = []
	for match in matches:
	    course_data.append({"label": match.name, "value": match.id})
	
	return json.dumps(course_data)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/recommendations/<username>')
def recommendations_for_user(username):
	user = models.User.find_by_username(username)
	return render_template('recommendations.html', recommendations=user.recommended_courses())

@app.route('/recommendations', methods=['POST'])
def recommendations():
	user = models.User.find_by_username(request.form['username'])
	if not user:
		user = models.User(username = request.form['username'])
		user.save()
	for key, value in request.form.items():
		m = re.match("course_(\d+)", key)
		if m:
			course_id = m.groups()[0]
			r = models.Ranking(course_id=course_id, user_id=user.id, value=value)
			r.save()
	return redirect("/recommendations/%s" % user.username)
		

@app.route('/logout')
def logout():
    if 'username' in session.keys():
        del session['username']
        return redirect('/')

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
