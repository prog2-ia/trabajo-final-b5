from src.entidades.excepciones_entidades import FormatoRitmoException


class Ritmo:
    def __init__(self, min_km: int, seg_km: int):
        if min_km < 0:
            raise FormatoRitmoException("Los minutos por kilómetro no pueden ser negativos.")

        if seg_km < 0 or seg_km > 59:
            raise FormatoRitmoException(f"Los segundos ({seg_km}) son inválidos. Deben estar entre 0 y 59.")

        self._min_km = min_km
        self._seg_km = seg_km