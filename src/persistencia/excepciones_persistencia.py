# src/excepciones/personalizadas.py

class FitnessAppException(Exception):
    pass

class PersistenciaException(FitnessAppException):
    """Se lanza ante errores de E/S o permisos en Linux """
    pass

class ArchivoCorruptoException(FitnessAppException):
    """Se lanza cuando un archivo binario está dañado o vacío """
    pass