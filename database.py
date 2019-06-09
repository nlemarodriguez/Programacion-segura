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
        self.cur.execute('SELECT c.id, c.texto, c.fecha, uu.nombres, uu.apellidos, uu.foto  from usuario u, usuario uu, comentario c where c.idusuario_comenta = u.id and '
                         'c.idusuario_postea = uu.id and u.id = %s order by c.fecha desc', id)
        result = self.cur.fetchall()
        return result


