from flask import render_template, request, flash, Blueprint
departments_blueprint = Blueprint('departments', __name__)
from models import *


@departments_blueprint.route('', methods=['GET', 'POST'])
def departments():
    """Loading departments list."""
    deps = Department.query.all()
    return render_template('departments.html', deps=deps)


@departments_blueprint.route('/<departmentid>', methods=['GET', 'POST'])
def department_page(departmentid):
    """Loading specific department info page."""
    department = Department.query.filter_by(id=departmentid).first()
    positions = Position.query.filter_by(idd=departmentid).all()
    poslist, workers = [], []
    for f in positions:
        poslist.append(f.id)  # creating list of id positions
    for idp in poslist:
        workers_temp = Worker.query.filter_by(idp=idp).all()
        workers = workers_temp + workers  # getting workers profile list
    return render_template('department_page.html', department=department, workers=workers)


@departments_blueprint.route('/new', methods=['GET', 'POST'])
def newdepartment():
    """Creating department page."""
    if request.method == 'POST':
        name, description = request.form['name'], request.form['description']
        db.session.add(Department(name, description))
        db.session.commit()
        flash("New Department was added")
    return render_template('newdepartment.html')


@departments_blueprint.route('/<departmentid>/change', methods=['GET', 'POST'])
def changedepartment(departmentid):
    """Page for changing department data."""
    dep = Department.query.filter_by(id=departmentid).first()
    if request.method == 'POST':
        dep.name = request.form['name']
        dep.description = request.form['description']
        db.session.commit()
        flash("Department data was changed")
    return render_template('change_department.html', dep=dep)
