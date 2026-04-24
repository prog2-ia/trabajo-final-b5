class PlanSemanal:
    """Clase para organizar la agenda de entrenamientos semanales"""

    def __init__(self, coleccion_dias: list, entrenamientos_previstos: list):
        self._coleccion_dias = coleccion_dias
        self._entrenamientos_previstos = entrenamientos_previstos

    @property
    def entrenamientos_previstos(self) -> list:
        """Devuelve la lista de entrenamientos programados"""
        return self._entrenamientos_previstos