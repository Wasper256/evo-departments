from app import app
from flask import Flask, render_template, request, flash, redirect, Blueprint
from flask_sqlalchemy import SQLAlchemy
from models import *

changedepartment = Blueprint('changedepartment', __name__, template_folder='templates')
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
        poch.name = request.form['name']
        poch.description = request.form['description']
        poch.idd = request.form['idd']  # needs improvig(in merge case)
        db.session.commit()
        flash("Position data was changed")
    return render_template('change_position.html', deps=deps, pos=pos)


@app.route('/vacancy/<vacancyid>/change', methods=['GET', 'POST'])
def changevacancy(vacancyid):
    """Page for changing vacancy data."""
    deps = Department.query.all()
    vac = Vacancy.query.filter_by(id=vacancyid).first()
    if request.method == 'POST' and 'input1' in request.form:
        name = request.form['name']
        idd = request.form['idd']
        flash("Please input position in department")
        return render_template("change_vacancy2.html", Position=Position, idd=idd, name=name)
    if request.method == 'POST' and 'input2' in request.form:
        vach = Vacancy.query.get(vacancyid)
        vach.name = request.form['isname']
        # vach.idd = request.form['isid']
        vach.idp = request.form['idp']
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
        woch.name = request.form['name']
        woch.surname = request.form['surname']
        woch.email = request.form['email']
        woch.phone = request.form['phone']
        bdate = request.form['bdate']
        woch.bdate = datetime.strptime(bdate, "%Y-%m-%d")
        db.session.commit()
        flash("Worker data was changed")
    return render_template('change_worker.html', worker=worker, dt=dt)
