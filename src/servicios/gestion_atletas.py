from src.entidades.deportista import Deportista
from src.entidades.mediapersonal import MediaCorporal
from src.entidades.objetivo import Objetivo
from src.entidades.recordpersonal import RecordPersonal
from src.entidades.ejercicio import Ejercicio


class GestionAtletas:
    """Servicio para gestionar el perfil, metas y récords del usuario"""

    def __init__(self) -> None:
        self._atletas = []
        self._historial_medidas = []
        self._metas = []
        self._records = []

    def registrar_atleta(self, nombre: str, peso: float, altura: float) -> Deportista:
        """Crea un deportista y lo guarda en el sistema"""
        nuevo = Deportista(nombre, peso, altura)
        self._atletas.append(nuevo)
        return nuevo

    def añadir_medida(self, medida: MediaCorporal) -> None:
        """Registra una nueva medición corporal"""
        self._historial_medidas.append(medida)

    def fijar_objetivo(self, meta: Objetivo) -> None:
        """Guarda un nuevo objetivo físico"""
        self._metas.append(meta)

    def actualizar_record(self, ej: Ejercicio, marca: float) -> None:
        """Crea o actualiza un récord personal para un ejercicio"""
        nuevo_record = RecordPersonal(ej, marca)
        self._records.append(nuevo_record)

    def obtener_resumen_atleta(self) -> str:
        """Devuelve un resumen de progreso del usuario"""
        return f"Metas activas: {len(self._metas)} | Récords: {len(self._records)}"
