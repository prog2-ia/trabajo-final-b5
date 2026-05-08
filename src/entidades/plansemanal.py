from src.excepciones.excepciones_entidades import PlanSemanalIncoherenteException


class PlanSemanal:
    def __init__(self, coleccion_dias: list, entrenamientos_previstos: list):

        if len(coleccion_dias) != len(entrenamientos_previstos):
            raise PlanSemanalIncoherenteException(
                f"Incoherencia: Has indicado {len(coleccion_dias)} días pero {len(entrenamientos_previstos)} rutinas."
            )

        self._coleccion_dias = coleccion_dias
        self._entrenamientos_previstos = entrenamientos_previstos

    @property
    def entrenamientos_previstos(self) -> list:
        return self._entrenamientos_previstos