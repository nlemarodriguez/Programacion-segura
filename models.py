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

  def __init__(self, id, nombres, apellidos, sexo, fechaNacimiento, foto):
    self.id = id
    self.nombresCompletos = nombres + " " + apellidos
    self.nombres = nombres
    self.apellidos = apellidos
    self.sexo = Sexo.from_code(sexo).value
    self.fechaNacimiento = fechaNacimiento
    self.foto = foto