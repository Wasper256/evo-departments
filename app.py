"""Main app file."""
from flask import Flask, render_template
from extentions import db
# importing blueprints
from departments.departments import departments_blueprint
from positions.positions import positions_blueprint
from vacancy.vacancy import vacancy_blueprint
from workers.workers import workers_blueprint
# configuring app
app = Flask(__name__)
app.secret_key = 'some_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///evo.db'
db.init_app(app)
# registrating blueprints
app.register_blueprint(departments_blueprint, url_prefix='/departments')
app.register_blueprint(positions_blueprint, url_prefix='/positions')
app.register_blueprint(vacancy_blueprint, url_prefix='/vacancy')
app.register_blueprint(workers_blueprint, url_prefix='/workers')


@app.route('/')
def home():
    """Loading main page."""
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
	"""Error 404 page."""
    return render_template('404.html')

if __name__ == '__main__':
    app.run()
