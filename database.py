from enums import EstadoInvitacion
from models import Amigo
import pymysql


class Database:
    def __init__(self):
        host = "remotemysql.com"
        user = "cZILIyFPs3"
        password = "vc1LR4Tt2k"
        db = "cZILIyFPs3"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()

    def infouser_by_id(self, id):
        self.cur.execute('SELECT * from usuario where id = %s', id)
        result = self.cur.fetchall()
        return result

    def login(self, email, password):
        self.cur.execute('SELECT id from usuario where correo = %s and password = %s', (email, password))
        result = self.cur.fetchall()
        return result

    def wallposts_by_user(self, id):
        self.cur.execute(
            'SELECT c.id, c.texto, c.fecha, u_postea.nombres, u_postea.apellidos, u_postea.foto, u_postea.id u_postea  from usuario u, usuario u_postea, comentario c where c.idusuario_comenta = u.id and '
            'c.idusuario_postea = u_postea.id and u.id = %s order by c.fecha desc', id)
        result = self.cur.fetchall()
        return result

    def insert_post(self, texto, idusuario_postea, idusuario_comenta):
        self.cur.execute("INSERT INTO comentario (texto, idusuario_postea, idusuario_comenta) VALUES (%s,%s,%s)",
                         (texto, idusuario_postea, idusuario_comenta))
        self.con.commit()

    def search_friends(self, idUser, friend):
        self.cur.execute('SELECT u.id, u.nombres, u.apellidos, u.sexo, u.fechaNacimiento, '
                         '  (select i.estado from invitacion i where i.idusuario_invita = %s and i.idusuario_invitado = u.id order by i.fecha desc limit 1) '
                         '      as estadoInvitacion, '
                                               '  u.foto '                                                                                                                                                                      'from usuario u '
                                               '  where lower(u.nombres) LIKE %s or '
                                               '      lower(u.apellidos) LIKE %s order by u.nombres desc',
                         (idUser, '%'+friend.lower()+'%', '%'+friend.lower()+'%'))
        result = self.cur.fetchall()
        friendList = []
        for row in result:
            friend = Amigo(row['id'], row['nombres'], row['apellidos'], row['sexo'], row['fechaNacimiento'],
                           row['estadoInvitacion'], row['foto'])
            print(friend.estadoInvitacion)
            friendList.append(friend)
        return friendList

    def registrar_post(self, first_name, last_name, email, password, gender, photo):
        self.cur.execute(
            "INSERT INTO usuario (nombres, apellidos, correo, password, sexo, foto) VALUES (%s,%s,%s,%s,%s,%s)",
            (first_name, last_name, email, password, gender, photo))
        self.con.commit()

    def verificar_correo(self, email):
        self.cur.execute('SELECT correo from usuario where correo = %s', email)
        result = self.cur.fetchall()
        print(result)
        if len(result) == 0:
            return False
        else:
            return True

    def delete_commet(self, id):
        self.cur.execute('DELETE from comentario where id = %s', id)
        self.con.commit()

    def invite_friend(self, idUsuarioLogueado, idUsuarioAgregar):
        self.cur.execute(
            "INSERT INTO invitacion (estado, idusuario_invita, idusuario_invitado) VALUES (%s,%s,%s)",
            (EstadoInvitacion.PENDIENTE.value, idUsuarioLogueado, idUsuarioAgregar)
        )
        self.con.commit()
