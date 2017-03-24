"""Here creating  DB models."""
from app import db
import datetime


class Department(db.Model):
    """docstring for ClassName."""

    __tablename__ = "department"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __init__(self, name, description):
        """initialization."""
        self.name = name
        self.description = description


class Position(db.Model):
    """docstring for ClassName."""

    __tablename__ = "position"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    idd = db.Column(db.Integer, nullable=False)  # id of department

    def __init__(self, name, description, idd):
        """initialization."""
        self.name = name
        self.description = description
        self.idd = idd


class Vacancy(db.Model):
    """docstring for ClassName."""

    __tablename__ = "vacancy"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    idp = db.Column(db.Integer, nullable=False)  # id of position

    def __init__(self, name, description, idp):
        """initialization."""
        self.name = name
        self.description = description
        self.idp = idp


class Worker(db.Model):
    """docstring for ClassName."""

    __tablename__ = "worker"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    surname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    bdate = db.Column(db.DateTime, nullable=False)  # birth date
    edate = db.Column(db.DateTime)  # employment date
    idp = db.Column(db.Integer)  # id of position
    ishead = db.Column(db.Boolean)

    def __init__(self, name, description):
        """initialization."""
        self.name = name
        self.description = description
