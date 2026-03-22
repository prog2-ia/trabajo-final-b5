class Serie:
    def __init__(self, repeticiones: int, peso: float): # Añadimos tipos
        self._repeticiones = repeticiones
        self._peso = peso

    @property
    def repeticiones(self) -> int:
        return self._repeticiones
