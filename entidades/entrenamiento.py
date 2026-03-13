from abc import ABC, abstractmethod

class Entrenamiento(ABC):
    def __init__(self, fecha, duracion: int, id_entreno: int):
        self._fecha = fecha
        self._duracion = duracion
        self._id_entreno = id_entreno

    @property
    def duracion(self):
        return self._duracion


    @duracion.setter
    def duracion(self,valor: int):
        if valor <= 0:
            raise print(f"La duración debe ser mayor que 0")
        self._duracion = valor
    @abstractmethod
    def calcular_rendimiento(self):
        pass
    def __str__(self):
        return f"Entrenamiento {self.id_entreno} - {self.fecha}"

class EntrenamientoFuerza(Entrenamiento):
    def __init__(self, fecha, duracion, peso_levantado, repeticiones, id_entreno):
        super().__init__(fecha, duracion, id_entreno)
        self._peso_levantado = peso_levantado
        self._repeticiones = repeticiones
    def calcular_rendimiento(self):
        return float(self._peso_levantado * self._repeticiones)


class EntrenamientoCardio(Entrenamiento):
    def __init__(self, fecha, duracion, distancia, ritmo_medio, id_entreno):
        super().__init__(fecha, duracion, id_entreno)
        self._distancia = distancia
        self._ritmo_medio = ritmo_medio



    def calcular_rendimiento(self):
        if self._duracion = 0:
            return 0.0
        return self._distancia


