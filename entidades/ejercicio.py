class Ejercicio:
    """
    Define un movimiento o actividad específica.
    Se utiliza como bloque de construcción para otras clases.
    """
    def __init__(self, nombre: str, grupo_muscular: str, descripcion: str) -> None:
        self._nombre = nombre
        self._grupo_muscular = grupo_muscular
        self._descripcion = descripcion

    @property
    def nombre(self) -> str:
        """Permite acceder al nombre del ejercicio de forma segura."""
        return self._nombre