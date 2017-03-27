from flask import render_template, request, flash, Blueprint
from datetime import datetime
vacancy_blueprint = Blueprint('vacancy', __name__, template_folder='vacancy/templates/')
from models import *


@vacancy_blueprint.route('', methods=['GET', 'POST'])
def vacancy():
    """Loading vacancy list."""
    vac = Vacancy.query.all()
    return render_template('vacancy.html', vac=vac)


@vacancy_blueprint.route('/<vacancyid>', methods=['GET', 'POST'])
def vacansy_page(vacancyid):
    """Loading specific vacancy info page."""
    vac = Vacancy.query.filter_by(id=vacancyid).first()
    work = Worker.query.filter_by(idp=None).all()
    pos = Position.query.filter_by(id=vac.idp).first()
    if request.method == 'POST' and 'add' in request.form:
        workerid = request.form['id']
        worker = Worker.query.get(workerid)
        worker.idp = vac.idp
        worker.edate = datetime.utcnow()
        db.session.commit()  # Changing worker data
        db.session.add(WHistory(vac.idp, workerid, datetime.utcnow()))
        db.session.commit()  # Adding worker history
        vc = Vacancy.query.get(vacancyid)
        vc.cldate, vc.oc = datetime.utcnow(), False
        db.session.commit()  # Changing vacancy data
        flash("Success! Worker profile is updated. Now vacancy is close.")
    # reactivation feature
    if request.method == 'POST' and 'reactivate' in request.form:
        vc = Vacancy.query.get(vacancyid)
        vc.stdate, vc.oc = datetime.utcnow(), True
        db.session.commit()
        flash("Successful reactivation of vacancy")
    return render_template('vacancy_page.html', vac=vac, pos=pos, work=work)


@vacancy_blueprint.route('/new', methods=['GET', 'POST'])
def newvacancy():
    """Creating vacancy page."""
    deps = Department.query.all()
    # two stages of creating, because positions depends on departments
    if request.method == 'POST' and 'input1' in request.form:  # first
        name, idd = request.form['name'], request.form['idd']
        flash("Please pick position in department")
        return render_template("newvacancy2.html", Position=Position, idd=idd, name=name)
    if request.method == 'POST' and 'input2' in request.form:  # second
        name, idp = request.form['isname'], request.form['idp']
        db.session.add(Vacancy(name, idp, datetime.utcnow(), None, True))
        db.session.commit()  # commit changes
        flash("Vacancy added")
    return render_template('newvacancy.html', deps=deps)


@vacancy_blueprint.route('/<vacancyid>/change', methods=['GET', 'POST'])
def changevacancy(vacancyid):
    """Page for changing vacancy data."""
    deps = Department.query.all()
    vac = Vacancy.query.filter_by(id=vacancyid).first()
    # two stages of changing, because positions depends on departments
    if request.method == 'POST' and 'input1' in request.form:  # first
        name, idd = request.form['name'], request.form['idd']
        flash("Please pick position in department")
        return render_template("change_vacancy2.html", vac=vac, Position=Position, idd=idd, name=name)
    if request.method == 'POST' and 'input2' in request.form:  # second
        vac.name, vac.idp = request.form['isname'], request.form['idp']
        db.session.commit()  # commit vacancy data
        flash("Vacancy data was changed")
    return render_template('change_vacancy.html', deps=deps, vac=vac)
