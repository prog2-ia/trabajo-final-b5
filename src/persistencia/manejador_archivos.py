import csv
import pickle
import os
from src.persistencia.excepciones_persistencia import PersistenciaException, ArchivoCorruptoException
class ManejadorArchivos:
    """Clase de utilidad para leer y escribir datos en disco (CSV y Pickle) """

    @staticmethod
    def __asegurar_directorio(nombre_archivo: str):
        """
        Garantiza que el directorio existe antes de escribir.
        Cumple con el Aspecto 5: Rutas y directorios coherentes.
        """
        directorio = os.path.dirname(nombre_archivo)
        if directorio and not os.path.exists(directorio):
            try:
                os.makedirs(directorio, exist_ok=True)
            except OSError as e:
                raise PersistenciaException(f"Error al crear el directorio {directorio}: {e}")

    @staticmethod
    def guardar_en_csv(nombre_archivo: str, datos: list, cabecera: list):
        """Guarda datos en CSV usando modos de acceso adecuados """
        ManejadorArchivos.__asegurar_directorio(nombre_archivo)
        try:

            with open(nombre_archivo, 'w', newline='', encoding='utf-8') as f:
                escritor = csv.DictWriter(f, fieldnames=cabecera)
                escritor.writeheader()
                escritor.writerows(datos)
        except IOError as e:

            raise PersistenciaException(f"Fallo al escribir el archivo CSV: {e}")

    @staticmethod
    def cargar_desde_csv(nombre_archivo: str) -> list:
        """Lee archivos de texto plano CSV """
        if not os.path.exists(nombre_archivo):
            return []
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as f:
                return list(csv.DictReader(f))
        except IOError as e:
            raise PersistenciaException(f"Error de lectura en el CSV: {e}")

    @staticmethod
    def guardar_binario(nombre_archivo: str, objeto):
        """Guarda objetos usando serialización Pickle """
        ManejadorArchivos.__asegurar_directorio(nombre_archivo)
        try:

            with open(nombre_archivo, 'wb') as f:
                pickle.dump(objeto, f)
        except (pickle.PickleError, IOError) as e:
            raise PersistenciaException(f"Error al serializar datos en {nombre_archivo}: {e}")

    @staticmethod
    def cargar_binario(nombre_archivo: str):
        """Carga datos binarios gestionando archivos corruptos o vacíos"""
        if not os.path.exists(nombre_archivo):
            return None
        try:
            with open(nombre_archivo, 'rb') as f:
                return pickle.load(f)
        except (pickle.UnpicklingError, EOFError):
            raise ArchivoCorruptoException(f"El archivo binario {nombre_archivo} está dañado.")
        except (IOError, PermissionError) as e:
            raise PersistenciaException(f"Error de acceso al archivo binario: {e}")

