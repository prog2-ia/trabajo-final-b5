class Deportista:
    def __init__(self, nombre: str, peso: float, altura: float):
        self.nombre = nombre
        self._peso = peso
        self._altura = altura

    @property
    def peso(self) -> float:
        return self._peso

    @peso.setter
    def peso(self, valor: float):
        if valor <= 0:
            raise ValueError("El peso debe ser positivo")
        self._peso = valor
