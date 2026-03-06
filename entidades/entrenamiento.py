class Entrenamiento:
    def __init__(self, fecha, duracion, id_entreno):
        self.fecha = fecha
        self.duracion = duracion
        self.id_entreno = id_entreno


    def calcular_rendimiento(self):
        pass

    def __str__(self):
        pass

class EntrenamientoFuerza(Entrenamiento):
    def __init__(self, fecha, duracion, peso_levantado, repeticiones, id_entreno)
        super().__init__(fecha, duracion, id_entreno)
        self.peso_levantado = peso_levantado
        self.repeticiones = repeticiones


class EntrenamientoCardio(Entrenamiento):
    def __init__(self, fecha, duracion, distancia, ritmo_medio, id_entreno)
        super().__init__(fecha, duracion, id_entreno)
        self.distancia = distancia
        self.ritmo_medio = ritmo_medio


