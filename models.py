"""Here is DB models."""
from app import db


class Department(db.Model):
    """Department model."""

    __tablename__ = "department"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __init__(self, name, description):
        """initialization."""
        self.name = name
        self.description = description


class Position(db.Model):
    """Position model."""

    __tablename__ = "position"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    idd = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)

    def __init__(self, name, description, idd):
        """initialization."""
        self.name = name
        self.description = description
        self.idd = idd


class Vacancy(db.Model):
    """Vacancy model."""

    __tablename__ = "vacancy"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    idp = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)
    stdate = db.Column(db.DateTime, nullable=False)  # open date
    cldate = db.Column(db.DateTime)  # close date
    oc = db.Column(db.Boolean)  # open or close

    def __init__(self, name, idp, stdate, cldate, oc):
        """initialization."""
        self.name = name
        self.idp = idp
        self.stdate = stdate
        self.cldate = cldate
        self.oc = oc


class Worker(db.Model):
    """Worker model."""

    __tablename__ = "worker"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    bdate = db.Column(db.DateTime, nullable=False)  # birth date
    edate = db.Column(db.DateTime)  # employment date
    idp = db.Column(db.Integer, db.ForeignKey('position.id'))  # id of position
    ishead = db.Column(db.Boolean, default=False)  # is this head of depatment?

    def __init__(self, name, surname, email, phone, bdate, edate, idp, ishead):
        """initialization."""
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone
        self.bdate = bdate
        self.edate = edate
        self.idp = idp
        self.ishead = ishead


class WHistory(db.Model):
    """Workers history model."""

    __tablename__ = "whistory"

    id = db.Column(db.Integer, primary_key=True)
    idp = db.Column(db.Integer, db.ForeignKey('position.id'))
    idw = db.Column(db.Integer, db.ForeignKey('worker.id'))
    edt = db.Column(db.DateTime, nullable=False)  # event date time

    def __init__(self, idp, idw, edt):
        """initialization."""
        self.idp = idp
        self.idw = idw
        self.edt = edt
