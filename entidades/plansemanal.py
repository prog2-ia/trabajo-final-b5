class PlanSemanal:
    def __init__(self, coleccion_dias: list, entrenamientos_previstos: list):
        self._coleccion_dias = coleccion_dias
        self._entrenamientos_previstos = entrenamientos_previstos

    @property
    def entrenamientos_previstos(self):
        return self._entrenamientos_previstos