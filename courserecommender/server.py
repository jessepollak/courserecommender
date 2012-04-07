import flask
from flask import Flask, g, render_template
from flaskext.sqlalchemy import SQLAlchemy
import itertools
import os

import database
import models

app = Flask(__name__)
db = models.init(os.environ.get("DATABASE_URL", "sqlite:///development.sqlite3"))

@app.before_request
def before_request():
	g.db = db()

@app.teardown_request
def teardown_request(exception=None):
	if hasattr(g, 'db'):
		g.db.close()

@app.route("/courses")
def courses_index():
	course_store = CourseStore(g.db)
	return repr(course_store.all())

@app.route('/')
def homepage():
    return render_template('homepage.html')

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)
