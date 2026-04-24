class Deportista:
    """
    Entidad que representa a un usuario del sistema.
    Almacena sus datos físicos básicos para el seguimiento.
    """
    def __init__(self, nombre: str, peso: float, altura: float) -> None:
        self._nombre = nombre  # Atributo protegido para asegurar el encapsulamiento
        self._peso = peso
        self._altura = altura

    @property
    def peso(self) -> float:
        """Getter: Devuelve el peso actual del deportista."""
        return self._peso

    @peso.setter
    def peso(self, valor: float) -> None:
        """Setter: Valida que el nuevo peso ingresado sea lógicamente correcto."""
        if valor <= 0:
            raise ValueError("El peso debe ser positivo")
        self._peso = valor

