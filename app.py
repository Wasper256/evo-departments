from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


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


@app.route('/departments/<departmentid>')
def department_page(departmentid):
    return render_template('departments.html')


@app.route('/positions/<positionid>')
def position_page(positionid):
    return render_template('positions.html')


@app.route('/vacansy/<vacancyid>')
def vacansy_page(vacancyid):
    return render_template('vacansy.html')


@app.route('/workers/<userid>')
def profile(userid):
    user = Worker.query.filter_by(id=userid).first()
    position = Position.query.filter_by(id=user.idp).first()
    return render_template('profile.html', user=user, position=position)


@app.route('/workers/new', methods=['GET', 'POST'])
def newworker():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        phone = request.form['phone']
        bdate = request.form['bdate']
        bdate = datetime.strptime(bdate, "%Y-%m-%d")
        db.session.add(Worker(name, surname, email, phone, bdate, None, None, False))
        db.session.commit()
        flash("New worker was added")
    return render_template('newworker.html')


@app.route('/departments/new', methods=['GET', 'POST'])
def newdepartment():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        db.session.add(Department(name, description))
        db.session.commit()
        flash("New Department was added")
    return render_template('newdepartment.html')


@app.route('/positions/new', methods=['GET', 'POST'])
def newposition():
    deps = Department.query.all()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        idd = request.form['idd']
        db.session.add(Position(name, description, idd))
        db.session.commit()
        flash("New Position was added")
    return render_template('newposition.html', deps=deps)


@app.route('/vacancy/new', methods=['GET', 'POST'])
def newvacancy():
    deps = Department.query.all()
    if request.method == 'POST' and 'input1' in request.form:
        name = request.form['name']
        idd = request.form['idd']
        flash("Please input position in department")
        return render_template("newvacancy2.html", Position=Position, idd=idd, name=name)
    if request.method == 'POST' and 'input2' in request.form:
        name = request.form['isname']
        idd = request.form['isid']
        idp = request.form['idp']
        db.session.add(Vacancy(name, idp, datetime.utcnow(), None, True))
        db.session.commit()
        flash("Vacancy added")
    return render_template('newvacancy.html', deps=deps)


if __name__ == '__main__':
    app.run(debug=True)
