from pymysql import connect

from enums import EstadoInvitacion
from models import Amigo, SolicitudAmigo, Comentario
import pymysql, api

con = None


class Database:

    def open_connection(self):
        global con
        if con is None or not con.open:
            host = "remotemysql.com"
            user = "cZILIyFPs3"
            password = "vc1LR4Tt2k"
            db = "cZILIyFPs3"
            con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                       DictCursor)
        
    def infouser_by_id(self, id):
        self.open_connection()
        cur = con.cursor()
        cur.execute('SELECT * from usuario where id = %s', id)
        result = cur.fetchall()
        return result

    def login(self, email, password):
        self.open_connection()
        cur = con.cursor()
        cur.execute('SELECT id from usuario where correo = %s and password = %s', (email, password))
        result = cur.fetchall()
        return result

    def wallposts_by_user(self, id):
        self.open_connection()
        cur = con.cursor()
        cur.execute(
            'SELECT c.id, c.texto, c.fecha, u_postea.nombres, u_postea.apellidos, u_postea.foto, u_postea.id u_postea, im.imagen  from usuario u, usuario u_postea, comentario c left join imagen im on im.id=c.idimagen where c.idusuario_comenta = u.id and '
            'c.idusuario_postea = u_postea.id and u.id = %s order by c.fecha desc', id)
        result = cur.fetchall()
        comentarios = []
        for row in result:
            cur.execute(
                'SELECT c.id, c.texto, c.fecha, u.nombres, u.apellidos, u.foto, u.id u_postea FROM comentario c, usuario u where idcomentario = %s and u.id = c.idusuario_postea order by c.fecha', row['id'])
            sub_comentarios = cur.fetchall()
            c = Comentario(row['id'], row['texto'], row['fecha'], row['nombres'], row['apellidos'], row['foto'], row['u_postea'], api.pretty_date(row['fecha']), row['imagen'], sub_comentarios)
            comentarios.append(c)
        return comentarios

    def insert_post(self, texto, idusuario_postea, idusuario_comenta, idImagen):
        self.open_connection()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO comentario (texto, idusuario_postea, idusuario_comenta, idimagen) VALUES (%s,%s,%s,%s)",
            (texto, idusuario_postea, idusuario_comenta, idImagen))
        con.commit()

    def insert_imagen(self, idFiltro, rutaImagen):
        self.open_connection()
        cur = con.cursor()
        cur.execute("INSERT INTO imagen (idfiltro, imagen) VALUES (%s,%s)",
                         (idFiltro, rutaImagen))
        idImagen = cur.lastrowid
        con.commit()
        return idImagen

    def search_friends(self, idUser, friend):
        self.open_connection()
        cur = con.cursor()
        cur.execute('SELECT u.id, u.nombres, u.apellidos, u.sexo, u.fechaNacimiento, '
                         '  (select i.estado from invitacion i where (i.idusuario_invita = %s and i.idusuario_invitado = u.id) or (i.idusuario_invitado = %s and i.idusuario_invita = u.id) order by i.fecha desc limit 1) '
                         '      as estadoInvitacion, '
                                               '  u.foto '                                                                                                                                                                      'from usuario u '
                                               '  where (lower(u.nombres) LIKE %s or '
                                               '      lower(u.apellidos) LIKE %s)'
                         '                              AND u.id != %s '
                         '                              order by u.nombres desc',
                         (idUser, idUser, '%'+friend.lower()+'%', '%'+friend.lower()+'%', idUser))
        result = cur.fetchall()
        friendList = []
        for row in result:
            amigo = Amigo(row['id'], row['nombres'], row['apellidos'], row['sexo'], row['fechaNacimiento'], row['estadoInvitacion'], row['foto'])
            friendList.append(amigo)
        return friendList

    def registrar_usuario(self, first_name, last_name, email, password, gender, photo):
        self.open_connection()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO usuario (nombres, apellidos, correo, password, sexo, foto) VALUES (%s,%s,%s,%s,%s,%s)",
            (first_name, last_name, email, password, gender, photo))
        con.commit()

    def verificar_correo(self, email):
        self.open_connection()
        cur = con.cursor()
        cur.execute('SELECT correo from usuario where correo = %s', email)
        result = cur.fetchall()
        if len(result) == 0:
            return False
        else:
            return True

    def delete_commet(self, id):
        self.open_connection()
        cur = con.cursor()
        cur.execute('DELETE from comentario where id = %s', id)
        con.commit()

    def invite_friend(self, idUsuarioLogueado, idUsuarioAgregar):
        self.open_connection()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO invitacion (estado, idusuario_invita, idusuario_invitado) VALUES (%s,%s,%s)",
            (EstadoInvitacion.PENDIENTE.value, idUsuarioLogueado, idUsuarioAgregar)
        )
        con.commit()

    def get_request_number(self, idUsuario):
        self.open_connection()
        cur = con.cursor()
        cur.execute('SELECT count(*) as total from invitacion i where i.idusuario_invitado = %s and i.estado =  %s',
                         (idUsuario, EstadoInvitacion.PENDIENTE.value)
        )
        result = cur.fetchone()
        return result

    def search_requests(self, idUser):
        self.open_connection()
        cur = con.cursor()
        cur.execute('SELECT i.id as idInvitacion, u.id as idUsuario, u.nombres, u.apellidos, u.sexo, u.fechaNacimiento, u.foto '
                         ' from usuario u join invitacion i on u.id = i.idusuario_invita '
                            '  WHERE i.idusuario_invitado = %s and i.estado = %s '
                         '      ORDER BY u.nombres desc',
                            (idUser, EstadoInvitacion.PENDIENTE.value)
                         )
        result = cur.fetchall()
        requests = []
        for row in result:
            s = SolicitudAmigo(row['idInvitacion'], row['idUsuario'], row['nombres'], row['apellidos'], row['sexo'], row['fechaNacimiento'], row['foto'])
            requests.append(s)
        return requests

    def friends_list(self, id):
        self.open_connection()
        cur = con.cursor()
        cur.execute(
            'SELECT invitado.id, invitado.nombres, invitado.apellidos, invitado.foto FROM usuario invita, usuario invitado, invitacion i WHERE i.idusuario_invita = invita.id and i.idusuario_invitado = invitado.id and i.estado = ' + str(EstadoInvitacion.ACEPTADO.value) + ' and invita.id = %s union ALL SELECT invita.id, invita.nombres, invita.apellidos, invita.foto FROM usuario invitado, usuario invita, invitacion i WHERE i.idusuario_invitado = invitado.id and i.idusuario_invita = invita.id and i.estado = ' + str(EstadoInvitacion.ACEPTADO.value) + ' and invitado.id = %s', (id, id))
        result = cur.fetchall()
        return result

    def estado_amistad(self, id_user, id_determinar):
        self.open_connection()
        cur = con.cursor()
        if id_user == id_determinar:
            return -1
        else:
            cur.execute("""
            select estado from invitacion where idusuario_invita = %s and idusuario_invitado = %s 
                               
            """, (id_user, id_determinar))
            result = cur.fetchone()
            if result is None:
                cur.execute("""
                select estado from invitacion where idusuario_invita = %s and idusuario_invitado = %s 
                """, (id_determinar, id_user))
                result1 = cur.fetchone()
                if result1 is None:
                    return EstadoInvitacion.NEUTRAL.value
                else:
                    valor = result1['estado']
                    if valor == 1:
                        return 5
                    else:
                        return valor
            else:
                return result['estado']

    def insert_comment_reply(self, id_comentario_padre, texto, id_usuario):
        self.open_connection()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO comentario (texto, idcomentario, idusuario_postea) VALUES (%s,%s,%s)",
            (texto, id_comentario_padre, id_usuario)
        )
        con.commit()

    def editar_usuario(self, first_name, last_name, email, gender, photo, fecha_nac, id):
        self.open_connection()
        cur = con.cursor()
        cur.execute(
            'UPDATE usuario SET nombres = %s, apellidos = %s, correo = %s, sexo = %s , foto = %s, fechaNacimiento = %s WHERE id = %s',
            (first_name, last_name, email, gender, photo, fecha_nac, id))
        con.commit()

    def accept_friend(self, idInvitation):
        self.open_connection()
        cur = con.cursor()
        cur.execute(
            'UPDATE invitacion SET estado = %s WHERE id = %s',
            (EstadoInvitacion.ACEPTADO.value, idInvitation)
        )
        con.commit()

    def refuse_friend(self, idInvitation):
        self.open_connection()
        cur = con.cursor()
        cur.execute(
            'UPDATE invitacion SET estado = %s WHERE id = %s',
            (EstadoInvitacion.RECHAZADO.value, idInvitation)
        )
        con.commit()

    def editar_contrasena(self, password, id):
        self.open_connection()
        cur = con.cursor()
        cur.execute(
            'UPDATE usuario SET password = %s WHERE id = %s', (password, id))
        con.commit()
