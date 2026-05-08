

class ServicioException(Exception):
    """Clase base para todas las excepciones de la capa de servicios (lógica de negocio)."""
    pass

class AtletaYaRegistradoException(ServicioException):
    """Se lanza al intentar registrar un deportista con un nombre que ya existe en el sistema."""
    pass

class CalculoImcException(ServicioException):
    """Se lanza cuando las matemáticas del IMC fallan (por ejemplo, altura no válida para el cálculo)."""
    pass

class EjercicioDuplicadoException(ServicioException):
    """Se lanza al intentar crear un ejercicio que ya se encuentra en el catálogo."""
    pass

class SesionInvalidaException(ServicioException):
    """Se lanza al intentar registrar un entrenamiento nulo o sin datos concretos."""
    pass