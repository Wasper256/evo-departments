from flask import Flask, render_template, request, flash, g
import sqlite3

app = Flask(__name__)
app.secret_key = 'some_secret'
app.database = "sample.db"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/departments')
def departments():
    return render_template('departments.html')


@app.route('/positions')
def positions():
    return render_template('positions.html')


@app.route('/vacansy')
def vacansy():
    return render_template('vacansy.html')


@app.route('/workers')
def workers():
    return render_template('workers.html')


@app.route('/workers/new', methods=['GET', 'POST'])
def newworker():
    with sqlite3.connect('sample.db') as g.db:
        error = None
        if request.method == 'POST':
            name = request.form['name']
            surname = request.form['surname']
            print(name)
            print(surname)
        return render_template('newworker.html', error=error)


def connect_db():
    return sqlite3.connect(app.database)


if __name__ == '__main__':
    app.run(debug=True)
