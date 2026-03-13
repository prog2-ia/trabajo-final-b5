[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/09uckVan)
# Gestor de Entrenamientos y Rendimiento 

## Descripción del Proyecto
Este proyecto es una aplicación de consola desarrollada en Python para la asignatura de **Programación II** del Grado en IA en la **Universidad de Alicante**. Su objetivo es permitir a deportistas registrar sus entrenamientos (Fuerza y Cardio), realizar un seguimiento de sus medidas corporales y visualizar su progreso hacia metas específicas.

## 👥 Integrantes del Equipo
* **Integrante 1**: Óscar Marco Albertos
* **Integrante 2**: Miguel Vicente Mollá
* **Grupo**: B5

## Arquitectura del Sistema
El sistema sigue una arquitectura profesional de 4 capas para garantizar la separación de responsabilidades:
1. **Entidades**: Clases puras que representan el dominio (Deportista, Entrenamiento, etc.).
2. **Servicios**: Lógica de negocio y cálculos de rendimiento.
3. **Persistencia**: Manejo de datos mediante ficheros CSV y Binarios (Pickle).
4. **UI**: Interfaz de usuario mediante menús interactivos por consola.

## Requisitos e Instalación
Para ejecutar este proyecto, es necesario tener instalado Python 3.12.3 y seguir estos pasos:

1. **Clonar el repositorio**:
   git clone [https://github.com/prog2-ia/trabajo-final-b5.git](https://github.com/prog2-ia/trabajo-final-b5.git)
   cd trabajo-final-b5

2. **Crear y activar el entorno virtual (venv)**:
 Windows: python -m venv venv y .\venv\Scripts\activate
 Linux/macOS: python -m venv venv y source venv/bin/activate

3. **Instalar dependencias**:
 pip install -r requirements.txt

## Uso
Para iniciar el gestor de entrenamientos, ejecuta el script principal desde la raíz del proyecto:
python main.py