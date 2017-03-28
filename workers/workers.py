"""File with all Workers backend."""
from flask import render_template, request, flash, redirect, Blueprint
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
workers_blueprint = Blueprint('workers', __name__)
from models import *


@workers_blueprint.route("", methods=['GET', 'POST'])
def workers():
    """Loading workers list."""
    workers = Worker.query.all()
    return render_template('workers.html', workers=workers)


@workers_blueprint.route('/new', methods=['GET', 'POST'])
def newworker():
    """Loading creating worker page."""
    if request.method == 'POST':
        try:  # backend email validation
            validate_email(request.form['email'], check_deliverability=False)
            try:  # simple user check
                email = request.form['email']
                name, surname = request.form['name'], request.form['surname']
                phone, bdate = request.form['phone'], request.form['bdate']
                try:  # time formatting
                    bdate = datetime.strptime(bdate, "%Y-%m-%d")
                except:  # fix for mozilla and IE users
                    bdate = datetime.strptime(bdate, "%d-%m-%Y")
                db.session.add(Worker(name, surname, email, phone, bdate, None, None, False))
                db.session.commit()  # commit changes
                return redirect("/workers", code=302)
            except:
                flash("Error! This email or phone number already registrated!")
        except EmailNotValidError as e:  # send error message
            flash("Error!{0}".format(e))
    return render_template('newworker.html')


@workers_blueprint.route('/<workerid>/change', methods=['GET', 'POST'])
def changeworker(workerid):
    """Page for changing worker data."""
    worker = Worker.query.filter_by(id=workerid).first()
    dt = datetime.date(worker.bdate)
    if request.method == 'POST':
        # unique email&phone test
        testm = Worker.query.filter_by(email=request.form['email']).first()
        testp = Worker.query.filter_by(phone=request.form['phone']).first()
        if testm and testm.email != worker.email or testp and testp.phone != worker.phone:
            flash("Error! Profile with this email or phone already exist!")
        else:  # writting data
            worker.name, worker.surname = request.form['name'], request.form['surname']
            worker.email, worker.phone = request.form['email'], request.form['phone']
            worker.bdate = datetime.strptime(request.form['bdate'], "%Y-%m-%d")
            db.session.commit()
            return redirect("workers/{0}".format(worker.id), code=302)
    return render_template('change_worker.html', worker=worker, dt=dt)


@workers_blueprint.route('/<userid>', methods=['GET', 'POST'])
def profile(userid):
    """Loading specific worker info page."""
    user = Worker.query.filter_by(id=userid).first()
    position = Position.query.filter_by(id=user.idp).first()
    deps = Department.query.all()
    whptable, whdtable, dep = ([] for i in range(3))
    wh = WHistory.query.filter_by(idw=userid).all()
    for i in wh:  # getting data for worker history table
        temppos = Position.query.filter_by(id=i.idp).first()
        tempdep = Department.query.filter_by(id=temppos.idd).first()
        whdtable.append(tempdep.name), whptable.append(temppos.name)
    if user.idp:
        dep = Department.query.filter_by(id=position.idd).first()
        if request.method == 'POST' and 'fireworker' in request.form:
            # fire this worker from current position
            prof = Worker.query.get(userid)
            prof.idp, prof.edate, prof.ishead = (None for x in range(3))
            db.session.commit()
        if request.method == 'POST' and 'moveworker' in request.form:
            # move worker in other department
            idd = request.form['idd']
            # new dwpartment position check
            odp = Position.query.filter_by(idd=idd, name=position.name).first()
            if not odp:  # existing same position check
                name, description = position.name, position.description
                db.session.add(Position(name, description, idd))
                db.session.commit()  # creating same position in new department
                odp = Position.query.filter_by(name=name, idd=idd).first()
            user.idp, user.edate = odp.id, datetime.utcnow()
            user.ishead = False  # "unheading"
            # writting worker history
            db.session.add(WHistory(user.idp, userid, datetime.utcnow()))
            db.session.commit()  # commit changes
            return redirect("/workers/{0}".format(userid), code=302)
        if request.method == 'POST' and 'makehead' in request.form:
            # make head of department
            positionsd = Position.query.filter_by(idd=dep.id).all()
            for p in positionsd:  # search for other head in this department
                workers = Worker.query.filter_by(idp=p.id, ishead=True).first()
                if workers:  # "unheading"
                    headmove, headmove.ishead = Worker.query.get(workers.id), False
            profile = Worker.query.get(userid)
            profile.ishead = True  # makig worker head of department
            db.session.commit()
    if request.method == 'POST' and 'deleteworker' in request.form:
        # delete worker
        Worker.query.filter_by(id=userid).delete()
        db.session.commit()
        return redirect("", code=302)
    return render_template('profile.html', user=user, position=position, dep=dep, deps=deps, wh=wh, whptable=whptable, whdtable=whdtable)
