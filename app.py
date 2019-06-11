import os
from flask import Flask, render_template, request, url_for, jsonify, flash, redirect, json, session
from flask_bootstrap import Bootstrap
from database import Database

URL_FOLDER = '/static/imagen_perfil/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static', 'imagen_perfil')

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
    print(comentarios_del_usuario)
    user = db.infouser_by_id(iduser)
    amigos = db.friends_list(iduser)
    print('los amigos son: ')
    print(amigos)
    return render_template('profile.html', user=user[0], comentarios=comentarios_del_usuario, amigos=amigos)

#Example: http://127.0.0.1:3000/search?friend=Maria
@app.route('/search')
def search():
    idUser = session.get('user_logged')
    friend = request.args['friend']
    print("User: "+str(idUser))
    print("Friend: "+str(friend))
    friends = db.search_friends(idUser, friend)
    print(friends)
    return render_template('search.html', friends=friends)


@app.route('/post_comment/<id>', methods=['POST'])
def post_comment(id):
    if request.method == 'POST':
        texto = request.form['texto_publicacion']
        idusuario_postea = session.get('user_logged')
        idusuario_comenta = id
        db.insert_post(texto, idusuario_postea, idusuario_comenta)
        return redirect(url_for('profile', user=idusuario_comenta))


@app.route('/registro')
def registro():
    return render_template('registro.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/registrar_usuario', methods=['POST'])
def reister():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        file = request.files['files[]']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photo = URL_FOLDER + file.filename
        else:
            if gender == 'F':
                photo = URL_FOLDER + 'woman-img.png'
            else:
                photo = URL_FOLDER + 'man-img.png'

        existeCorreo = db.verificar_correo(email)
        if existeCorreo:
            flash('Usuario ya existe')
            return render_template('registro.html')
        else:
            db.registrar_post(first_name, last_name, email, password, gender, photo)
            flash('Usuario registrado con éxito')
            return redirect(url_for('index'))

@app.route('/delete_commmet/<id>', methods=['POST', 'GET'])
def delete_commet(id):
    db.delete_commet(id)
    return redirect(url_for('profile', user=session.get('user_logged')))


@app.route('/invite/<idInvitado>', methods=['POST'])
def invite_friend(idInvitado):
    if request.method == 'POST':
        idUsuarioLogueado = session.get('user_logged')
        db.invite_friend(idUsuarioLogueado, idInvitado)
        info = db.infouser_by_id(idInvitado)[0]
        flash('Invitación de amistad enviada exitosamente a << ' + (info['nombres']+" "+info['apellidos'] + ' >>'))
        return redirect(request.referrer)

@app.route('/requests')
def requests():
    idUser = session.get('user_logged')
    requests = db.search_requests(idUser)
    print(requests)
    return render_template('requests.html', requests=requests)

if __name__ == '__main__':
    app.run(port=3000, debug=True)
