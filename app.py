"""Main app file."""
from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from email_validator import validate_email

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


@app.route('/departments', methods=['GET', 'POST'])
def departments():
    """Loading departments list."""
    deps = Department.query.all()
    return render_template('departments.html', deps=deps)


@app.route('/positions', methods=['GET', 'POST'])
def positions():
    """Loading positions list."""
    pos = Position.query.all()
    return render_template('positions.html', pos=pos)


@app.route('/vacancy', methods=['GET', 'POST'])
def vacancy():
    """Loading vacancy list."""
    vac = Vacancy.query.all()
    return render_template('vacancy.html', vac=vac)


@app.route('/workers', methods=['GET', 'POST'])
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
    vac = Vacancy.query.filter_by(id=vacancyid).first()
    work = Worker.query.filter_by(idp=None).all()
    pos = Position.query.filter_by(id=vac.idp).first()
    if request.method == 'POST' and 'add' in request.form:
        workerid = request.form['id']
        # Changing worker data
        worker = Worker.query.get(workerid)
        worker.idp = vac.idp
        worker.edate = datetime.utcnow()
        db.session.commit()
        # Adding worker history
        db.session.add(WHistory(vac.idp, workerid, datetime.utcnow()))
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
    return render_template('vacancy_page.html', vac=vac, pos=pos, work=work)


@app.route('/workers/<userid>', methods=['GET', 'POST'])
def profile(userid):
    """Loading specific worker info page."""
    user = Worker.query.filter_by(id=userid).first()
    position = Position.query.filter_by(id=user.idp).first()
    deps = Department.query.all()
    whptable, whdtable, dep = ([] for i in range(3))
    wh = WHistory.query.filter_by(idw=userid).all()
    for i in wh:
        temppos = Position.query.filter_by(id=i.idp).first()
        tempdep = Department.query.filter_by(id=temppos.idd).first()
        whdtable.append(tempdep.name), whptable.append(temppos.name)
    if user.idp:
        dep = Department.query.filter_by(id=position.idd).first()
        if request.method == 'POST' and 'fireworker' in request.form:
            prof = Worker.query.get(userid)
            prof.idp, prof.edate, prof.ishead = (None for x in range(3))
            db.session.commit()
        if request.method == 'POST' and 'moveworker' in request.form:
            idd = request.form['idd']
            # new dwpartment position check
            odp = Position.query.filter_by(idd=idd, name=position.name).first()
            if not odp:
                name, description = position.name, position.description
                db.session.add(Position(name, description, idd))
                db.session.commit()
                odp = Position.query.filter_by(name=name, idd=idd).first()
            profile = Worker.query.get(userid)
            profile.idp, profile.edate = odp.id, datetime.utcnow()
            profile.ishead = False
            db.session.add(WHistory(profile.idp, userid, datetime.utcnow()))
            db.session.commit()
            return redirect("/workers/{0}".format(userid), code=302)
        if request.method == 'POST' and 'makehead' in request.form:
            positionsd = Position.query.filter_by(idd=dep.id).all()
            for p in positionsd:
                workers = Worker.query.filter_by(idp=p.id, ishead=True).first()
                if workers:
                    headmove, headmove.ishead = Worker.query.get(workers.id), False
            profile = Worker.query.get(userid)
            profile.ishead = True
            db.session.commit()
    if request.method == 'POST' and 'deleteworker' in request.form:
        Worker.query.filter_by(id=userid).delete()
        db.session.commit()
        return redirect("/workers", code=302)
    return render_template('profile.html', user=user, position=position, dep=dep, deps=deps, wh=wh, whptable=whptable, whdtable=whdtable)


@app.route('/departments/new', methods=['GET', 'POST'])
def newdepartment():
    """Creating department page."""
    if request.method == 'POST':
        name, description = request.form['name'], request.form['description']
        db.session.add(Department(name, description))
        db.session.commit()
        flash("New Department was added")
    return render_template('newdepartment.html')


@app.route('/positions/new', methods=['GET', 'POST'])
def newposition():
    """Creating position page."""
    deps = Department.query.all()
    if request.method == 'POST':
        name, idd = request.form['name'], request.form['idd']
        description = request.form['description']
        db.session.add(Position(name, description, idd))
        db.session.commit()
        flash("New Position was added")
    return render_template('newposition.html', deps=deps)


@app.route('/vacancy/new', methods=['GET', 'POST'])
def newvacancy():
    """Creating vacancy page."""
    deps = Department.query.all()
    if request.method == 'POST' and 'input1' in request.form:
        name, idd = request.form['name'], request.form['idd']
        flash("Please input position in department")
        return render_template("newvacancy2.html", Position=Position, idd=idd, name=name)
    if request.method == 'POST' and 'input2' in request.form:
        name, idp = request.form['isname'], request.form['idp']
        db.session.add(Vacancy(name, idp, datetime.utcnow(), None, True))
        db.session.commit()
        flash("Vacancy added")
    return render_template('newvacancy.html', deps=deps)


@app.route('/workers/new', methods=['GET', 'POST'])
def newworker():
    """Loading creating worker page."""
    if request.method == 'POST':
        name, surname = request.form['name'], request.form['surname']
        phone, bdate = request.form['phone'], request.form['bdate']
        bdate = datetime.strptime(bdate, "%Y-%m-%d")
        try:
            val = validate_email(request.form['email'])
            email = val["email"]
            db.session.add(Worker(name, surname, email, phone, bdate, None, None, False))
            db.session.commit()
            flash("New worker was added")
        except:
            flash("Wrong email format!")
    return render_template('newworker.html')


@app.route('/departments/<departmentid>/change', methods=['GET', 'POST'])
def changedepartment(departmentid):
    """Page for changing department data."""
    dep = Department.query.filter_by(id=departmentid).first()
    if request.method == 'POST':
        dech = Department.query.get(departmentid)
        dech.name = request.form['name']
        dech.description = request.form['description']
        db.session.commit()
        flash("Department data was changed")
    return render_template('change_department.html', dep=dep)


@app.route('/positions/<positionid>/change', methods=['GET', 'POST'])
def changeposition(positionid):
    """Page for changing position data."""
    deps = Department.query.all()
    pos = Position.query.filter_by(id=positionid).first()
    if request.method == 'POST':
        poch = Position.query.get(positionid)
        poch.name, poch.idd = request.form['name'], request.form['idd']
        poch.description = request.form['description']
        db.session.commit()
        flash("Position data was changed")
    return render_template('change_position.html', deps=deps, pos=pos)


@app.route('/vacancy/<vacancyid>/change', methods=['GET', 'POST'])
def changevacancy(vacancyid):
    """Page for changing vacancy data."""
    deps = Department.query.all()
    vac = Vacancy.query.filter_by(id=vacancyid).first()
    if request.method == 'POST' and 'input1' in request.form:
        name, idd = request.form['name'], request.form['idd']
        flash("Please input position in department")
        return render_template("change_vacancy2.html", vac=vac, Position=Position, idd=idd, name=name)
    if request.method == 'POST' and 'input2' in request.form:
        vach = Vacancy.query.get(vacancyid)
        vach.name, vach.idp = request.form['isname'], request.form['idp']
        db.session.commit()
        flash("Vacancy data was changed")
    return render_template('change_vacancy.html', deps=deps, vac=vac)


@app.route('/workers/<workerid>/change', methods=['GET', 'POST'])
def changeworker(workerid):
    """Page for changing worker data."""
    worker = Worker.query.filter_by(id=workerid).first()
    dt = datetime.date(worker.bdate)
    if request.method == 'POST':
        woch = Worker.query.get(workerid)
        woch.name, woch.surname = request.form['name'], request.form['surname']
        woch.email, woch.phone = request.form['email'], request.form['phone']
        woch.bdate = datetime.strptime(request.form['bdate'], "%Y-%m-%d")
        db.session.commit()
        return redirect("/workers/{0}".format(worker.id), code=302)
    return render_template('change_worker.html', worker=worker, dt=dt)


if __name__ == '__main__':
    app.run(debug=True)
