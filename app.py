"""Main app file."""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from departments.departments import departments_blueprint
from positions.positions import positions_blueprint
from vacancy.vacancy import vacancy_blueprint
from workers.workers import workers_blueprint

app = Flask(__name__)
app.secret_key = 'some_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///evo.db'
# create the sqlalchemy object
db = SQLAlchemy(app)
# import db schema

app.register_blueprint(departments_blueprint, url_prefix='/departments')
app.register_blueprint(positions_blueprint, url_prefix='/positions')
app.register_blueprint(vacancy_blueprint, url_prefix='/vacancy')
app.register_blueprint(workers_blueprint, url_prefix='/workers')


@app.route('/')
def home():
    """Loading main page."""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

# @simple_page.errorhandler(404)
# def page_not_found(e):
#     return render_template('pages/404.html')
