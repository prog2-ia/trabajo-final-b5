# test_servicios.py

from src.servicios.gestion_deportiva import GestionDeportiva
from src.entidades.entrenamiento import EntrenamientoFuerza, EntrenamientoCardio
from src.entidades.ritmo import Ritmo


def probar_capa_servicios():
    """Script para validar que la lógica de negocio funciona correctamente."""

    print("=== INICIANDO TEST DE LA CAPA DE SERVICIOS (GRUPO B5) ===")

    # 1. Instanciar el servicio principal (El "Cerebro")
    gestor = GestionDeportiva()

    # 2. Probar alta de deportistas y lógica de IMC
    # El servicio orquesta la creación de entidades
    print("\n[Paso 1: Gestión de Atletas]")
    atleta1 = gestor.dar_alta_deportista("Oscar", 82.5, 1.80)
    atleta2 = gestor.dar_alta_deportista("Miguel", 76.0, 1.75)

    imc_medio = gestor.calcular_imc_promedio()
    print(f"Atletas registrados: {atleta1._nombre} y {atleta2._nombre}")
    print(f"IMC Promedio calculado: {imc_medio}")

    # 3. Probar registro de entrenamientos (Herencia y Polimorfismo)
    # Registramos una sesión de Fuerza y una de Cardio  [cite: 6, 132-134]
    print("\n[Paso 2: Registro de Entrenamientos]")

    # Fuerza: fecha, duracion, peso, repeticiones, id
    entreno_f = EntrenamientoFuerza("2024-05-22", 60, 120.5, 10, 101)
    gestor.registrar_entrenamiento(entreno_f)

    # Cardio: fecha, duracion, distancia, ritmo, id
    ritmo_carrera = Ritmo(5, 15)  # 5:15 min/km
    entreno_c = EntrenamientoCardio("2024-05-23", 40, 7.5, ritmo_carrera, 102)
    gestor.registrar_entrenamiento(entreno_c)

    print("Sesiones de Fuerza y Cardio registradas en el historial.")

    # 4. Verificar resumen y polimorfismo
    print("\n[Paso 3: Verificación de Resultados]")
    print(gestor.obtener_resumen_sistema())

    # Comprobamos que el cálculo de rendimiento funciona para cada tipo
    for e in gestor._historial_entrenamientos:
        print(f"ID {e._id_entreno}: Rendimiento calculado = {e.calcular_rendimiento()}")

    print("\n=== TEST FINALIZADO CON ÉXITO ===")


if __name__ == "__main__":
    probar_capa_servicios()