import os


from flask import Flask
from flas import render_template
from flaskext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:development.sqlite3")
db = SQLAlchemy(app)

@app.route('/')
def hello():
    return render_template('course.html', name ="Elephant")

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)