

class EntidadException(Exception):
    """Clase base para todas las excepciones lógicas de las entidades."""
    pass

class ValorFisicoInvalidoException(EntidadException):
    """Para atributos físicos (peso, altura, repeticiones) con valores imposibles."""
    pass

class AtributoVacioException(EntidadException):
    """Para cuando se intentan crear entidades sin nombre o descripción obligatoria."""
    pass

class PorcentajeInvalidoException(EntidadException):
    """Para porcentajes lógicamente incorrectos (menores a 0 o mayores a 100)"""
    pass

class FormatoRitmoException(EntidadException):
    """Para cuando un ritmo tiene más de 59 segundos o valores ilógicos."""
    pass

class PlanSemanalIncoherenteException(EntidadException):
    """Para cuando no coinciden los días seleccionados con los entrenamientos asignados."""
    pass

class FechaPasadaException(EntidadException):
    """Para cuando se establece un objetivo con una fecha que ya ha expirado."""
    pass