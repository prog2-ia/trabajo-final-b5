from src.entidades.excepciones_entidades import PorcentajeInvalidoException, ValorFisicoInvalidoException


class MediaCorporal:
    def __init__(self, fecha: str, grasa: float, peso: float) -> None:
        self._fecha = fecha

        if not (0 <= grasa <= 100):

            raise PorcentajeInvalidoException(f"El porcentaje de grasa ({grasa}%) es irreal. Debe estar entre 0 y 100.")
        self._grasa = grasa

        if peso <= 0:
            raise ValorFisicoInvalidoException("El peso registrado en la medición debe ser mayor a cero.")
        self._peso = peso