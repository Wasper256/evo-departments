from flask import render_template, request, flash, redirect, Blueprint
from datetime import datetime
workers_blueprint = Blueprint('workers', __name__)
from models import Department, Worker, Position


@workers_blueprint.route('/new', methods=['GET', 'POST'])
def newworker():
    """Loading creating worker page."""
    if request.method == 'POST':
        name, surname = request.form['name'], request.form['surname']
        phone, bdate = request.form['phone'], request.form['bdate']
        email = request.form['email']
        bdate = datetime.strptime(bdate, "%Y-%m-%d")
        try:
            db.session.add(Worker(name, surname, email, phone, bdate, None, None, False))
            db.session.commit()
            return redirect("", code=302)
        except:
            flash("Error! This email or phone number already registrated!")
    return render_template('newworker.html')


@workers_blueprint.route('/<workerid>/change', methods=['GET', 'POST'])
def changeworker(workerid):
    """Page for changing worker data."""
    worker = Worker.query.filter_by(id=workerid).first()
    dt = datetime.date(worker.bdate)
    if request.method == 'POST':
        worker.name, worker.surname = request.form['name'], request.form['surname']
        worker.email, worker.phone = request.form['email'], request.form['phone']
        worker.bdate = datetime.strptime(request.form['bdate'], "%Y-%m-%d")
        db.session.commit()
        return redirect("/{0}".format(worker.id), code=302)
    return render_template('change_worker.html', worker=worker, dt=dt)


@workers_blueprint.route('/<userid>', methods=['GET', 'POST'])
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
        return redirect("", code=302)
    return render_template('profile.html', user=user, position=position, dep=dep, deps=deps, wh=wh, whptable=whptable, whdtable=whdtable)


@workers_blueprint.route('', methods=['GET', 'POST'])
def workers():
    """Loading workers list."""
    workers = Worker.query.all()
    return render_template('workers.html', workers=workers)
