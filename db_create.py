"""Creating DB."""
import datetime
from app import db
from models import Department, Position, Vacancy, Worker

db.create_all()
db.session.add(Department("Lazy dep", "Department for lazy workers"))
db.session.add(Position("Nothing to do", "Just read the instructions", 1))
db.session.add(Vacancy("Lazy commander", 1, datetime.datetime.utcnow(), datetime.datetime.utcnow(), True))
db.session.add(Worker("Adolf", "Kitler", "adi@ss.com", "+380989154774", datetime.datetime.utcnow(), datetime.datetime.utcnow(), 1, True))
db.session.commit()
