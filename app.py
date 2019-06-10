from flask import Flask, render_template, request, url_for, jsonify, flash, redirect, json, session
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
            session['user_logged'] = userid[0]['id']
            return redirect(url_for('profile', user=userid[0]['id']))
        else:
            flash('El usuario no existe')
            return redirect(url_for('index'))


@app.route('/profile')
def profile():
    iduser = request.args['user']
    comentarios_del_usuario = db.wallposts_by_user(iduser)
    user = db.infouser_by_id(iduser)
    return render_template('profile.html', user=user[0], comentarios=comentarios_del_usuario)


@app.route('/post_comment/<id>', methods=['POST'])
def post_comment(id):
    if request.method == 'POST':
        texto = request.form['texto_publicacion']
        idusuario_postea = session.get('user_logged')
        idusuario_comenta = id
        db.insert_post(texto, idusuario_postea, idusuario_comenta)
        return redirect(url_for('profile', user=idusuario_comenta))


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
