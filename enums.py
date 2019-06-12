from enum import Enum

class EstadoInvitacion(Enum):
    NEUTRAL = 0
    PENDIENTE = 1
    ACEPTADO = 2
    RECHAZADO = 3
    ELIMINADO = 4

class Sexo(Enum):
    MASCULINO = 'Masculino'
    FEMENINO = 'Femenino'

    @staticmethod
    def from_code(label):
        if label in ('M'):
            return Sexo.MASCULINO
        elif label in ('F'):
            return Sexo.FEMENINO
        else:
            raise NotImplementedError
