import os
from src.entidades.entrenamiento import Entrenamiento, EntrenamientoFuerza, EntrenamientoCardio
from src.entidades.plansemanal import PlanSemanal
from src.entidades.ejercicio import Ejercicio
from src.entidades.serie import Serie
from src.entidades.ritmo import Ritmo
from src.persistencia.manejador_archivos import ManejadorArchivos

class GestionEntrenamientos:
    """Servicio para gestionar la actividad física y la planificación"""

    def __init__(self) -> None:
        self._ejercicios_disponibles = []
        self._historial_sesiones = []
        self._planes = []


    def cargar_estado(self):
        """Carga los entrenamientos guardados"""
        datos = ManejadorArchivos.cargar_binario("data/sesiones.pkl")
        if datos:
            self._historial_sesiones = datos

    def guardar_estado(self):
        """Guarda los entrenamientos realizados"""
        os.makedirs("data", exist_ok=True)
        ManejadorArchivos.guardar_binario("data/sesiones.pkl", self._historial_sesiones)


    def crear_ejercicio(self, nombre: str, grupo: str, desc: str) -> Ejercicio:
        nuevo = Ejercicio(nombre, grupo, desc)
        self._ejercicios_disponibles.append(nuevo)
        return nuevo

    def registrar_entrenamiento(self, sesion: Entrenamiento) -> None:
        self._historial_sesiones.append(sesion)

    def programar_semana(self, dias: list, entrenos: list) -> None:
        nuevo_plan = PlanSemanal(dias, entrenos)
        self._planes.append(nuevo_plan)

    def crear_serie_fuerza(self, reps: int, peso: float) -> Serie:
        return Serie(reps, peso)

    def definir_ritmo_cardio(self, mins: int, segs: int) -> Ritmo:
        return Ritmo(mins, segs)