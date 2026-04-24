class Serie:
    """Representa un conjunto de repeticiones con un peso específico"""

    def __init__(self, repeticiones: int, peso: float):
        self._repeticiones = repeticiones
        self._peso = peso

    @property
    def repeticiones(self) -> int:
        return self._repeticiones
