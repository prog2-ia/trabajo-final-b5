import os
from src.entidades.deportista import Deportista
from src.entidades.mediapersonal import MediaCorporal
from src.entidades.objetivo import Objetivo
from src.entidades.recordpersonal import RecordPersonal
from src.entidades.ejercicio import Ejercicio
from src.persistencia.manejador_archivos import ManejadorArchivos

class GestionAtletas:
    """Servicio para gestionar el perfil, metas y récords del usuario"""

    def __init__(self) -> None:
        self._atletas = []
        self._historial_medidas = []
        self._metas = []
        self._records = []


    def cargar_estado(self):
        """Carga los datos guardados al iniciar el programa"""
        datos = ManejadorArchivos.cargar_binario("data/atletas.pkl")
        if datos:
            self._atletas = datos

    def guardar_estado(self):
        """Guarda los datos antes de cerrar el programa"""
        os.makedirs("data", exist_ok=True)
        ManejadorArchivos.guardar_binario("data/atletas.pkl", self._atletas)

    # --- TU CÓDIGO ORIGINAL (Intacto) ---
    def registrar_atleta(self, nombre: str, peso: float, altura: float) -> Deportista:
        nuevo = Deportista(nombre, peso, altura)
        self._atletas.append(nuevo)
        return nuevo

    def añadir_medida(self, medida: MediaCorporal) -> None:
        self._historial_medidas.append(medida)

    def fijar_objetivo(self, meta: Objetivo) -> None:
        self._metas.append(meta)

    def actualizar_record(self, ej: Ejercicio, marca: float) -> None:
        nuevo_record = RecordPersonal(ej, marca)
        self._records.append(nuevo_record)

    def obtener_resumen_atleta(self) -> str:
        return f"Metas activas: {len(self._metas)} | Récords: {len(self._records)}"


    def obtener_todos(self) -> list:
        return self._atletas

    def calcular_imc_atleta(self, atleta: Deportista) -> float:
        """Calcula el Índice de Masa Corporal"""
        if atleta._altura > 0:
            return round(atleta._peso / (atleta._altura ** 2), 2)
        return 0.0