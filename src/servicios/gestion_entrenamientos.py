from src.entidades.entrenamiento import Entrenamiento, EntrenamientoFuerza, EntrenamientoCardio
from src.entidades.plansemanal import PlanSemanal
from src.entidades.ejercicio import Ejercicio
from src.entidades.serie import Serie
from src.entidades.ritmo import Ritmo


class GestionEntrenamientos:
    """Servicio para gestionar la actividad física y la planificación"""

    def __init__(self) -> None:
        self._ejercicios_disponibles = []
        self._historial_sesiones = []
        self._planes = []

    def crear_ejercicio(self, nombre: str, grupo: str, desc: str) -> Ejercicio:
        """Añade un ejercicio al catálogo del sistema"""
        nuevo = Ejercicio(nombre, grupo, desc)
        self._ejercicios_disponibles.append(nuevo)
        return nuevo

    def registrar_entrenamiento(self, sesion: Entrenamiento) -> None:
        """Guarda una sesión realizada (Fuerza o Cardio)"""
        self._historial_sesiones.append(sesion)

    def programar_semana(self, dias: list, entrenos: list) -> None:
        """Crea una nueva planificación semanal"""
        nuevo_plan = PlanSemanal(dias, entrenos)
        self._planes.append(nuevo_plan)

    def crear_serie_fuerza(self, reps: int, peso: float) -> Serie:
        """Crea una serie de trabajo (usado en lógica de Fuerza)"""
        return Serie(reps, peso)

    def definir_ritmo_cardio(self, mins: int, segs: int) -> Ritmo:
        """Crea un objeto de ritmo para sesiones de carrer[cite: 17]"""
        return Ritmo(mins, segs)
