from datetime import date
from src.excepciones.excepciones_entidades import FechaPasadaException, AtributoVacioException


class Objetivo:
    def __init__(self, tipo_meta: str, valor_objetivo: float, fecha_limite: date):
        if not tipo_meta.strip():
            raise AtributoVacioException("El tipo de meta no puede estar vacío.")

        # Error lógico: viajes en el tiempo
        if fecha_limite < date.today():
            raise FechaPasadaException(f"La fecha límite ({fecha_limite}) ya ha pasado. Define una meta a futuro.")

        self._tipo_meta = tipo_meta
        self._valor_objetivo = valor_objetivo
        self._fecha_limite = fecha_limite

    @property
    def tipo_meta(self) -> str:
        return self._tipo_meta