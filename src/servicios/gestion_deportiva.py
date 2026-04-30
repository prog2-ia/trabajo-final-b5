from entidades.deportista import Deportista
from entidades.entrenamiento import Entrenamiento, EntrenamientoFuerza, EntrenamientoCardio


class GestionDeportiva:
    """
    Clase de servicio que gestiona la lógica de negocio del sistema.
    Controla las listas de atletas y entrenamientos, y realiza cálculos.
    """

    def __init__(self):
        # Listas protegidas para almacenar los datos en memoria
        self._atletas = []  # Almacenará objetos de tipo Deportista
        self._historial_entrenamientos = []  # Almacenará objetos de tipo Entrenamiento

    def dar_alta_deportista(self, nombre: str, peso: float, altura: float) -> Deportista:
        """Crea un nuevo deportista y lo añade a la gestión."""
        nuevo_atleta = Deportista(nombre, peso, altura)
        self._atletas.append(nuevo_atleta)
        return nuevo_atleta

    def registrar_entrenamiento(self, entrenamiento: Entrenamiento):
        """Añade un entrenamiento al historial general."""
        self._historial_entrenamientos.append(entrenamiento)

    def obtener_todos_los_entrenamientos(self) -> list:
        """Devuelve la lista completa de sesiones registradas."""
        return self._historial_entrenamientos

    def calcular_imc_deportista(self, atleta: Deportista) -> float:
        """
        Calcula el Índice de Masa Corporal de un atleta.
        Fórmula: peso / altura^2
        """
        # Accedemos a la altura (protegida) y al peso (propiedad)
        # Nota: atleta._altura se usa porque no definimos getter para altura aún
        return round(atleta.peso / (atleta._altura ** 2), 2)

    def filtrar_entrenamientos_fuerza(self) -> list:
        """Filtra y devuelve solo las sesiones de fuerza usando polimorfismo."""
        fuerza = []
        for e in self._historial_entrenamientos:
            if isinstance(e, EntrenamientoFuerza):
                fuerza.append(e)
        return fuerza

    def obtener_resumen_estadistico(self) -> dict:
        """Calcula estadísticas básicas sobre los entrenamientos realizados."""
        total_sesiones = len(self._historial_entrenamientos)
        total_fuerza = len(self.filtrar_entrenamientos_fuerza())
        total_cardio = total_sesiones - total_fuerza

        return {
            "total": total_sesiones,
            "fuerza": total_fuerza,
            "cardio": total_cardio
        }

