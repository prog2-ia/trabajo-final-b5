class Ejercicio:
    def __init__(self, nombre: str, grupo_muscular: str, descripcion: str):
        self._nombre = nombre
        self._grupo_muscular = grupo_muscular
        self._descripcion = descripcion

    @property
    def nombre(self) -> str:
        return self._nombre