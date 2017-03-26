"""Main app file."""
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
    """Loading main page."""
    return render_template('index.html')


@app.route('/departments')
def departments():
    """Loading departments list."""
    deps = Department.query.all()
    return render_template('departments.html', deps=deps)


@app.route('/positions')
def positions():
    """Loading positions list."""
    pos = Position.query.all()
    return render_template('positions.html', pos=pos)


@app.route('/vacancy')
def vacancy():
    """Loading vacancy list."""
    vac = Vacancy.query.all()
    return render_template('vacancy.html', vac=vac)


@app.route('/workers')
def workers():
    """Loading workers list."""
    workers = Worker.query.all()
    return render_template('workers.html', workers=workers)


@app.route('/departments/<departmentid>', methods=['GET', 'POST'])
def department_page(departmentid):
    """Loading specific department info page."""
    department = Department.query.filter_by(id=departmentid).first()
    positions = Position.query.filter_by(idd=departmentid).all()
    poslist, workers = [], []
    for f in positions:
        poslist.append(f.id)
    for idp in poslist:
        workers_temp = Worker.query.filter_by(idp=idp).all()
        workers = workers_temp + workers
    return render_template('department_page.html', department=department, workers=workers)


@app.route('/positions/<positionid>', methods=['GET', 'POST'])
def position_page(positionid):
    """Loading specific position info page."""
    position = Position.query.filter_by(id=positionid).first()
    dep = Department.query.filter_by(id=position.idd).first()
    return render_template('position_page.html', position=position, dep=dep)


@app.route('/vacancy/<vacancyid>', methods=['GET', 'POST'])
def vacansy_page(vacancyid):
    """Loading specific vacancy info page."""
    vacancy = Vacancy.query.filter_by(id=vacancyid).first()
    workers = Worker.query.filter_by(idp=None).all()
    position = Position.query.filter_by(id=vacancy.idp).first()
    if request.method == 'POST' and 'add' in request.form:
        workerid = request.form['id']
        print(workerid)
        # Changing worker data
        worker = Worker.query.get(workerid)
        worker.idp = vacancy.idp
        worker.edate = datetime.utcnow()
        db.session.commit()
        # Adding worker history
        db.session.add(WHistory(vacancy.idp, workerid, datetime.utcnow()))
        db.session.commit()
        # Changing vacancy data
        vc = Vacancy.query.get(vacancyid)
        vc.cldate = datetime.utcnow()
        vc.oc = False
        db.session.commit()
        flash("Success! Worker profile is updated. Now vacancy is close.")
    if request.method == 'POST' and 'reactivate' in request.form:
        vc = Vacancy.query.get(vacancyid)
        vc.stdate = datetime.utcnow()
        vc.oc = True
        db.session.commit()
        flash("Successful reactivation of vacancy")
    return render_template('vacancy_page.html', vacancy=vacancy, position=position, workers=workers)


@app.route('/workers/<userid>', methods=['GET', 'POST'])
def profile(userid):
    """Loading specific worker info page."""
    user = Worker.query.filter_by(id=userid).first()
    position = Position.query.filter_by(id=user.idp).first()
    if request.method == 'POST' and 'deleteworker' in request.form:
        pass
    if request.method == 'POST' and 'firedworker' in request.form:
        pass
    if request.method == 'POST' and 'move worker' in request.form:
        pass
    if request.method == 'POST' and 'makehead' in request.form:
        pass
    return render_template('profile.html', user=user, position=position)


@app.route('/departments/new', methods=['GET', 'POST'])
def newdepartment():
    """Loading creating department page."""
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        db.session.add(Department(name, description))
        db.session.commit()
        flash("New Department was added")
    return render_template('newdepartment.html')


@app.route('/positions/new', methods=['GET', 'POST'])
def newposition():
    """Loading creating position page."""
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
    """Loading creating vacancy page."""
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


@app.route('/workers/new', methods=['GET', 'POST'])
def newworker():
    """Loading creating worker page."""
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


if __name__ == '__main__':
    app.run(debug=True)
