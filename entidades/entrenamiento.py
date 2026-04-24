from abc import ABC, abstractmethod


class Entrenamiento(ABC):
    """
    Clase abstracta base. No se puede instanciar directamente.
    Define el contrato común para todos los tipos de entrenamiento.
    """

    def __init__(self, fecha: str, duracion: int, id_entreno: int) -> None:
        self._fecha = fecha
        self._duracion = duracion
        self._id_entreno = id_entreno

    @property
    def duracion(self) -> int:
        """Devuelve la duración del entrenamiento en minutos."""
        return self._duracion

    @duracion.setter
    def duracion(self, valor: int) -> None:
        """Impide que se registre un entrenamiento con duración cero o negativa."""
        if valor <= 0:
            raise ValueError("La duración debe ser mayor que 0")
        self._duracion = valor

    @abstractmethod
    def calcular_rendimiento(self) -> float:
        """Método abstracto: cada clase hija debe definir cómo se calcula su rendimiento."""
        pass

    def __str__(self) -> str:
        """Representación en texto legible del objeto."""
        return f"Entrenamiento {self._id_entreno} - {self._fecha}"

class EntrenamientoFuerza(Entrenamiento):
    """
    Especialización (Herencia) para sesiones de levantamiento de peso.
    """
    def __init__(self, fecha: str, duracion: int, peso_levantado: float, repeticiones: int, id_entreno: int) -> None:
        super().__init__(fecha, duracion, id_entreno)
        self._peso_levantado = peso_levantado
        self._repeticiones = repeticiones

    def calcular_rendimiento(self) -> float:
        """
        Calcula el volumen total movido (Polimorfismo).
        Fórmula: peso levantado * repeticiones.
        """
        return float(self._peso_levantado * self._repeticiones)


class EntrenamientoCardio(Entrenamiento):
    """
    Especialización (Herencia) para sesiones de resistencia cardiovascular.
    """
    def __init__(self, fecha: str, duracion: int, distancia: float, ritmo_medio: 'Ritmo', id_entreno: int) -> None:
        super().__init__(fecha, duracion, id_entreno)
        self._distancia = distancia
        self._ritmo_medio = ritmo_medio

    def calcular_rendimiento(self) -> float:
        """
        Calcula el rendimiento basado en la distancia (Polimorfismo).
        Evita la división por cero si la duración es nula.
        """
        if self._duracion == 0:
            return 0.0
        return float(self._distancia)


