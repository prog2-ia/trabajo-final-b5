from datetime import date
from entidades.deportista import Deportista
from entidades.ejercicio import Ejercicio
from entidades.entrenamiento import EntrenamientoFuerza, EntrenamientoCardio
from entidades.mediapersonal import MediaCorporal
from entidades.objetivo import Objetivo
from entidades.plansemanal import PlanSemanal
from entidades.recordpersonal import RecordPersonal
from entidades.ritmo import Ritmo
from entidades.serie import Serie

print("--- EJECUTANDO PRUEBA DE ENTIDADES (GRUPO B5) ---")

# 1. Deportista
user = Deportista("Óscar", 80.0, 1.85)
print(f"Deportista: {user.nombre} | Peso: {user.peso}kg")

# 2. Ejercicio
ej = Ejercicio("Sentadilla", "Pierna", "Flexión de rodilla con barra")
s1 = Serie(10, 80.5)
print(f"Ejercicio: {ej._nombre} | Serie: {s1._repeticiones} reps")

# 3. Entrenamientos
# Fuerza
fuerza = EntrenamientoFuerza(date.today(), 45, 1200.0, 1, 1)
print(f"{fuerza} | Rendimiento Fuerza: {fuerza.calcular_rendimiento()}")

# Cardio
mi_ritmo = Ritmo(4, 50)
cardio = EntrenamientoCardio(date.today(), 30, 5.2, mi_ritmo, 2)
print(f"{cardio} | Rendimiento Cardio: {cardio.calcular_rendimiento()} km")

# 4. Seguimiento y Objetivos
medida = MediaCorporal(date.today(), 14.5, 79.5)
meta = Objetivo("Definición", 12.0, date(2026, 6, 1))
record = RecordPersonal(ej, 100.0)
print(f"Objetivo: {meta._tipo_meta} | Record en {record.ejercicio._nombre}: {record.mejor_marca}kg")

# 5. Planificación
mi_plan = PlanSemanal(["Lunes", "Viernes"], [fuerza, cardio])
print(f"Planificación: {len(mi_plan.entrenamientos_previstos)} entrenamientos programados.")

print("--- TODAS LAS CLASES INSTANCIADAS CORRECTAMENTE ---")