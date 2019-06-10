from enums import Sexo

class Amigo(object):

  def __init__(self, id, nombres, apellidos, sexo, fechaNacimiento, sonAmigos):
    self.id = id
    self.nombresCompletos = nombres + " " + apellidos
    self.nombres = nombres
    self.apellidos = apellidos
    self.sexo = Sexo.from_code(sexo).value
    self.fechaNacimiento = fechaNacimiento
    self.sonAmigos = sonAmigos