from flask import Flask, render_template, request, url_for, jsonify
from flask_bootstrap import Bootstrap
from database import Database


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app


app = create_app()
db = Database()


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        iduser = db.login(email, password)
        print(iduser)
        return jsonify(iduser)


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
    app.run(port=3000, debug=True)
