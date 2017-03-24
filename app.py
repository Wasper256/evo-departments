from flask import Flask, render_template, request, flash, g
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'some_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///evo.db'
# create the sqlalchemy object
db = SQLAlchemy(app)

# import db schema
from models import *


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/departments')
def departments():
    return render_template('departments.html')


@app.route('/positions')
def positions():
    return render_template('positions.html')


@app.route('/vacansy')
def vacansy():
    return render_template('vacansy.html')


@app.route('/workers')
def workers():
    return render_template('workers.html')


@app.route('/profile/<userid>')
def profile(userid):
    user = Worker.query.filter_by(id=userid).first()
    position = Position.query.filter_by(id=user.idp).first()
    return render_template('profile.html', user=user, position=position)


@app.route('/workers/new', methods=['GET', 'POST'])
def newworker():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        print(name)
        print(surname)
    return render_template('newworker.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)
