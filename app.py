from flask import Flask, render_template, request, url_for, jsonify, flash, redirect
from flask_bootstrap import Bootstrap
from database import Database


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app


app = create_app()
db = Database()
# settings
app.secret_key = "mysecretkey"

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = db.login(email, password)
        if user:
            return redirect(url_for('profile', user=user[0]))
        else:
            flash('El usuario no existe')
            return redirect(url_for('index'))


@app.route('/profile')
def profile():
    user = request.args.get('user')
    print(user)
    
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
