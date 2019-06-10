from flask import Flask, render_template, request, url_for, jsonify, flash, redirect, json
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
        userid = db.login(email, password)
        if userid:
            return redirect(url_for('profile', user=userid[0]['id']))
        else:
            flash('El usuario no existe')
            return redirect(url_for('index'))


@app.route('/profile')
def profile():
    iduser = request.args['user']
    print(iduser)
    comentarios_del_usuario = db.wallposts_by_user(iduser)
    user = db.infouser_by_id(iduser)
    print(comentarios_del_usuario)
    print(user)
    return render_template('profile.html', user=user[0], comentarios=comentarios_del_usuario)

#Example: http://127.0.0.1:3000/search?user=1&friend=Maria
@app.route('/search')
def search():
    idUser = request.args['user']
    friend = request.args['friend']
    print("User: "+str(idUser))
    print("Friend: "+str(friend))
    friends = db.search_friends(idUser, friend)
    print(friends)
    return render_template('search.html', friends = friends)


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
