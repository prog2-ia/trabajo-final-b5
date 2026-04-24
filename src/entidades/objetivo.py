class Objetivo:
    """Representa una meta física a alcanzar en una fecha determinada"""
    def __init__(self, tipo_meta: str, valor_objetivo: float, fecha_limite: date):
        self._tipo_meta = tipo_meta
        self._valor_objetivo = valor_objetivo
        self._fecha_limite = fecha_limite

    @property
    def tipo_meta(self) -> str:
        return self._tipo_meta

