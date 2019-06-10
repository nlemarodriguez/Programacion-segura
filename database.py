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
            'SELECT c.id, c.texto, c.fecha, uu.nombres, uu.apellidos, uu.foto  from usuario u, usuario uu, comentario c where c.idusuario_comenta = u.id and '
            'c.idusuario_postea = uu.id and u.id = %s order by c.fecha desc', id)
        result = self.cur.fetchall()
        return result

#, (select count(*) from invitacion i where i.idusuario_invita = %s and i.idusuario_invitado = u.id ) as friends
    def search_friends(self, idUser, friend):
        self.cur.execute('SELECT u.id, u.nombres, u.apellidos, u.sexo, u.fechaNacimiento, '
                         '  (select count(*) > 0 from invitacion i where i.idusuario_invita = %s and i.idusuario_invitado = u.id and i.estado = ' + str(EstadoInvitacion.ACEPTADO.value) +') as sonAmigos '
                         '  from usuario u '
                         '  where u.nombres LIKE %s or '
                         '      u.apellidos LIKE %s order by u.nombres desc', (idUser, friend, friend))
        result = self.cur.fetchall()
        friendList = []
        for row in result:
            friend = Amigo(row['id'], row['nombres'], row['apellidos'], row['sexo'], row['fechaNacimiento'], row['sonAmigos'])
            friendList.append(friend)
        return friendList


