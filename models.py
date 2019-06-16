from enums import Sexo, EstadoInvitacion

class Amigo(object):

  def __init__(self, id, nombres, apellidos, sexo, fechaNacimiento, estadoInvitacion, foto):
    self.id = id
    self.nombresCompletos = nombres + " " + apellidos
    self.nombres = nombres
    self.apellidos = apellidos
    self.sexo = Sexo.from_code(sexo).value
    self.fechaNacimiento = fechaNacimiento
    self.estadoInvitacion = estadoInvitacion
    self.sonAmigos = (EstadoInvitacion.ACEPTADO.value == estadoInvitacion)
    self.invitacionPendiente = (EstadoInvitacion.PENDIENTE.value == estadoInvitacion)
    self.foto = foto

class SolicitudAmigo(object):

  def __init__(self, idInvitacion, idUsuario, nombres, apellidos, sexo, fechaNacimiento, foto):
    self.idInvitacion = idInvitacion
    self.idUsuario = idUsuario
    self.nombresCompletos = nombres + " " + apellidos
    self.nombres = nombres
    self.apellidos = apellidos
    self.sexo = Sexo.from_code(sexo).value
    self.fechaNacimiento = fechaNacimiento
    self.foto = foto


class Comentario(object):

  def __init__(self, id, texto, fecha, nombres, apellidos, foto, u_postea, pretty_date, imagen, sub_comentarios):
    self.id = id
    self.texto = texto
    self.fecha = fecha
    self.nombres = nombres
    self.apellidos = apellidos
    self.u_postea = u_postea
    self.foto = foto
    self.pretty_date = pretty_date
    self.imagen = imagen
    self.sub_comentarios = sub_comentarios
