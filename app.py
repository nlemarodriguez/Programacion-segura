from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from database import Database
import pymysql


def create_app():
  app = Flask(__name__)
  Bootstrap(app)
  return app

app = create_app()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/users')
def users():
    def db_query():
        db = Database()
        emps = db.list_users()
        return emps
    res = db_query()
    return str(res)
    #return render_template('employees.html', result=res, content_type='application/json')

if __name__ == '__main__':
    app.run(port = 3000, debug = True)