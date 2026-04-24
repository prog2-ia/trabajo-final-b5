class MediaCorporal:
    """
    Registro histórico de la composición corporal del deportista.
    Útil para realizar un seguimiento del progreso a lo largo del tiempo.
    """
    def __init__(self, fecha: str, grasa: float, peso: float) -> None:
        self._fecha = fecha
        self._grasa = grasa
        self._peso = peso