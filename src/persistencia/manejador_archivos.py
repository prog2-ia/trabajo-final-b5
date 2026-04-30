import csv
import pickle
import os

class ManejadorArchivos:
    """Clase de utilidad para leer y escribir datos en disco (CSV y Pickle)"""

    @staticmethod
    def guardar_en_csv(nombre_archivo: str, datos: list, cabecera: list):
        """Guarda una lista de diccionarios en un archivo CSV"""
        with open(nombre_archivo, 'w', newline='', encoding='utf-8') as f:
            escritor = csv.DictWriter(f, fieldnames=cabecera)
            escritor.writeheader()
            escritor.writerows(datos)

    @staticmethod
    def cargar_desde_csv(nombre_archivo: str) -> list:
        """Lee un archivo CSV y devuelve una lista de diccionarios"""
        if not os.path.exists(nombre_archivo):
            return []
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            return list(csv.DictReader(f))

    @staticmethod
    def guardar_binario(nombre_archivo: str, objeto):
        """Guarda cualquier objeto Python (listas, clases) usando Pickle"""
        with open(nombre_archivo, 'wb') as f:
            pickle.dump(objeto, f)

    @staticmethod
    def cargar_binario(nombre_archivo: str):
        """Carga un objeto desde un archivo binario Pickle"""
        if not os.path.exists(nombre_archivo):
            return None
        with open(nombre_archivo, 'rb') as f:
            return pickle.load(f)