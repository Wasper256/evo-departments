"""File with all Positions backend."""
from flask import render_template, request, flash, redirect, Blueprint
positions_blueprint = Blueprint('positions', __name__)
from models import *


@positions_blueprint.route('', methods=['GET', 'POST'])
def positions():
    """Loading positions list."""
    pos = Position.query.all()
    return render_template('positions.html', pos=pos, deps=Department)


@positions_blueprint.route('/<positionid>', methods=['GET', 'POST'])
def position_page(positionid):
    """Loading specific position info page."""
    position = Position.query.filter_by(id=positionid).first()
    dep = Department.query.filter_by(id=position.idd).first()
    return render_template('position_page.html', position=position, dep=dep)


@positions_blueprint.route('/new', methods=['GET', 'POST'])
def newposition():
    """Creating position page."""
    deps = Department.query.all()
    if request.method == 'POST':
        name, idd = request.form['name'], request.form['idd']
        # some anticlone logic
        if not Position.query.filter_by(name=name, idd=idd).first():
            db.session.add(Position(name, request.form['description'], idd))
            db.session.commit()
            flash("New Position was added")
        else:
            flash("Error! This position already exist!")
    return render_template('newposition.html', deps=deps)


@positions_blueprint.route('/<positionid>/change', methods=['GET', 'POST'])
def changeposition(positionid):
    """Page for changing position data."""
    pos = Position.query.filter_by(id=positionid).first()
    deps = Department.query.all()
    if request.method == 'POST':
        poch = Position.query.filter_by(id=positionid).first()
        spos = Position.query.filter_by(idd=request.form['idep'], name=request.form['name']).first()
        if spos:  # if exist same position in same department:
            # move all to clone, first one - delete
            for p in Worker.query.filter_by(idp=pos.id).all():  # idp workers
                p.idp = spos.id
                db.session.commit()  # update idp workers
            for m in Vacancy.query.filter_by(idp=pos.id).all():  # idp vacancy
                m.idp = spos.id
                db.session.commit()  # update idp vacancy
            for o in WHistory.query.filter_by(idp=pos.id).all():  # idp WH
                o.idp = spos.id
                db.session.commit()  # update idp WHistory
            Position.query.filter_by(id=positionid).delete()  # remove old pos
        else:  # writing data
            poch.name, poch.idd = request.form['name'], request.form['idep']
            poch.description = request.form['description']
        db.session.commit()  # commit changes
        return redirect("", code=302)
    return render_template('change_position.html', deps=deps, pos=pos)
