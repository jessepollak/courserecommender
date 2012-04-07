import flask, json
from flask import Flask, g, render_template, request, session, redirect, url_for
from flaskext.sqlalchemy import SQLAlchemy
import itertools
import os

import database
import models

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!j4mNLWX/,?RT'
db = models.init(os.environ.get("DATABASE_URL", "sqlite:///development.sqlite3"))

def _get_user():
    return g.db.query(models.User).filter(models.User.username==request.form['username'])[0]

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
	    course_data.append(match.name)
	
	return json.dumps(course_data)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == "POST":
        print g.db.query(models.User).filter(models.User.username==request.form['username'])
        user = g.db.query(models.User).filter(models.User.username==request.form['username']).count()
        if not user:
            new_user = models.User(username=request.form['username'])
            g.db.add(new_user)
            g.db.commit()
        session['username'] = request.form['username']
        return redirect('/')
    else:
        return render_template('auth.html', auth_in_progress=True)

@app.route('/logout')
def logout():
    if 'username' in session.keys():
        del session['username']
        return redirect('/')

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)
