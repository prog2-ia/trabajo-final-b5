from entidades.ejercicio import Ejercicio

class RecordPersonal:
    def __init__(self, ejercicio: Ejercicio, mejor_marca: float):
        self._ejercicio = ejercicio
        self._mejor_marca = mejor_marca

    @property
    def ejercicio(self) -> Ejercicio:
        return self._ejercicio

    @property
    def mejor_marca(self) -> float:
        return self._mejor_marca

    @mejor_marca.setter
    def mejor_marca(self, valor: float):
        if valor < 0:
            raise ValueError("La mejor marca no puede ser negativa")
        self._mejor_marca = valor

    def __str__(self) -> str:
        return f"Récord en {self._ejercicio.nombre}: {self._mejor_marca}kg"