import os
from flask import Flask, render_template, request, url_for, jsonify, flash, redirect, json, session
from flask_bootstrap import Bootstrap
from database import Database
import uuid
from filters import pylibfromcpp
from filters import pylibfromcpp_mono_color, pylibfromcpp_3
import random
import time
import shutil

URL_FOLDER = '/static/imagen_perfil/'
URL_COMMENTS_FOLDER = '/static/imagen_comentarios/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static', 'imagen_perfil')
COMMENTS_UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static', 'imagen_comentarios/original')
COMMENTS_UPLOAD_MAIN_FOLDER = os.path.join(APP_ROOT, 'static', 'imagen_comentarios')

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['COMMENTS_UPLOAD_FOLDER'] = COMMENTS_UPLOAD_FOLDER
    app.config['COMMENTS_UPLOAD_MAIN_FOLDER'] = COMMENTS_UPLOAD_MAIN_FOLDER
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
            requestNumber = db.get_request_number(userid[0]['id'])['total']
            print(requestNumber)
            session['request_number'] = requestNumber
            session['user_logged'] = userid[0]['id']
            return redirect(url_for('profile', user=userid[0]['id']))
        else:
            flash('El usuario no existe')
            return redirect(url_for('index'))


@app.route('/profile')
def profile():
    iduser = int(request.args['user'])
    comentarios_del_usuario = db.wallposts_by_user(iduser)
    user = db.infouser_by_id(iduser)
    amigos = db.friends_list(iduser)
    #Determina el estado de amistad con el perfil que se está consultando
    estado_amistad = db.estado_amistad(session.get('user_logged'), iduser)
    propio_perfil = False

    if iduser == session.get('user_logged'):
        propio_perfil = True

    print('esAmigo/popioPerfil: '+str(estado_amistad)+'/'+str(propio_perfil))
    return render_template('profile.html', user=user[0], comentarios=comentarios_del_usuario, amigos=amigos,
                           estado_amistad=estado_amistad, propio_perfil=propio_perfil)


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
        file = request.files['imagenComentario']
        idImagen = None
        if file.filename != '':
            idImagen = save_comment_image(file)
        idusuario_postea = session.get('user_logged')
        idusuario_comenta = id
        db.insert_post(texto, idusuario_postea, idusuario_comenta, idImagen)
        return redirect(url_for('profile', user=idusuario_comenta))

def save_comment_image(file):
    print(file)
    oldFileName, fileExtension = file.filename.split('.')
    ##fileName = str(uuid.uuid4()) + "." + fileExtension #Random IDs
    fileName = str(random.randint(1000000,9000000)) + "." + fileExtension
    efectoImagen = request.form['efectoImagen']
    print(efectoImagen)

    if str(efectoImagen) == "4":
        file.save(os.path.join(app.config['COMMENTS_UPLOAD_MAIN_FOLDER'], fileName))
    else:
        file2 = open(os.path.join(app.config['COMMENTS_UPLOAD_FOLDER'], fileName), "wb")
        #file2.write(str(file.stream.read()))
        shutil.copyfileobj(file, file2)
        file2.close()
    if True: #TOdo validar los efectos
        try:
            if str(efectoImagen) != "4": #Sin Filtro = 4
                print(efectoImagen == "1")
                if str(efectoImagen) == "1":
                    print("Creando imagen Blanco y Negro")
                    pylibfromcpp.filter_image(fileName)
                else:
                    if str(efectoImagen) == "2":
                        print("Creando imagen Mono")
                        pylibfromcpp_mono_color.filter_image(fileName)
                    else:
                        pylibfromcpp_3.filter_image(fileName)
        except:
            print("Error filtros de imagen")
    imagenComentario = URL_COMMENTS_FOLDER + fileName
    print(imagenComentario)

    idImagen = db.insert_imagen(efectoImagen, imagenComentario)
    return idImagen


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

        existe_correo = db.verificar_correo(email)
        if existe_correo:
            flash('Usuario ya existe')
            return render_template('registro.html')
        else:
            db.registrar_usuario(first_name, last_name, email, password, gender, photo)
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


@app.route('/reply_comment/<id_comentario_padre>', methods=['POST'])
def reply_comment(id_comentario_padre):
    if request.method == 'POST':
        texto = request.form['comment']
        db.insert_comment_reply(id_comentario_padre, texto, session.get('user_logged'))
        return redirect(request.referrer)

@app.route('/editarDatos')
def editar_datos():
    id_user = session.get('user_logged')
    datos_usuario = db.infouser_by_id(id_user)[0]
    return render_template('edit_user.html', datosUsuario=datos_usuario)

        
@app.route('/editar_usuario', methods=['POST'])
def editar_usuario():
    if request.method == 'POST':
        id_user = session.get('user_logged')
        datos_usuario = db.infouser_by_id(id_user)[0]
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        gender = request.form['gender']
        fecha_nac = request.form['fechaNac']
        file = request.files['files[]']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photo = URL_FOLDER + file.filename
        else:
            photo = datos_usuario['foto']

        db.editar_usuario(first_name, last_name, email, gender, photo, fecha_nac, id_user)
        flash('Se editaron los datos con éxito')
        return redirect(url_for('editar_datos'))

@app.route('/acceptFriend/<idInvitation>', methods=['POST'])
def accept_friend(idInvitation):
    if request.method == 'POST':
        try:
            db.accept_friend(idInvitation)
            session['request_number'] = session['request_number'] - 1
            flash('Invitación aceptada exitosamente!', category='success')
        except:
            flash('Ha ocurrido un error al aceptar la invitación!', category='error')
        return redirect(request.referrer)

@app.route('/refuseFriend/<idInvitation>', methods=['POST'])
def refuse_friend(idInvitation):
    if request.method == 'POST':
        try:
            db.refuse_friend(idInvitation)
            session['request_number'] = session['request_number'] - 1
            flash('Invitación de amistad rechazada!', category='warning')
        except:
            flash('Ha ocurrido un error al rechazar la invitación!', category='error')
        return redirect(request.referrer)

@app.route('/editarPassword')
def editar_password():
    id_user = session.get('user_logged')
    return render_template('edit_password.html', id_user=id_user)

@app.route('/editar_pass', methods=['POST'])
def editar_pass():
    if request.method == 'POST':
        id_user = session.get('user_logged')
        datos_usuario = db.infouser_by_id(id_user)[0]
        password = datos_usuario['password']
        password_new = request.form['password_nueva']
        password_repeat = request.form['password_repetida']
        if request.form['password'] == password:
            if password_new == password_repeat:
                db.editar_contrasena(password_new, id_user)
                flash('El cambio de contraseña se realizó con éxito')
                return redirect(request.referrer)
            else:
                flash('Las contraseñas no coinciden')
                return redirect(request.referrer)
        else:
            flash('Las contraseñas no coinciden')
            return redirect(request.referrer)


if __name__ == '__main__':
    app.run(port=3000, debug=True)
