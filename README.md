

## 📖 Descripción del Proyecto
Este proyecto es una aplicación de escritorio avanzada con Interfaz Gráfica de Usuario (GUI) desarrollada en Python para la asignatura de **Programación II** del Grado en Inteligencia Artificial en la **Universidad de Alicante**.

Su objetivo es proporcionar a los entrenadores y deportistas una herramienta profesional para registrar entrenamientos (Fuerza y Cardio), realizar un seguimiento evolutivo de la biometría (IMC, Peso, Grasa), establecer un plan semanal y visualizar el progreso general a través de un ranking de rendimiento.

## 👥 Integrantes del Equipo
* **Integrante 1**: Óscar Marco Albertos
* **Integrante 2**: Miguel Vicente Mollá
* **Grupo**: B5

---

## 🏗️ Arquitectura del Sistema
El sistema sigue una **arquitectura profesional de 4 capas** estructurada mediante Programación Orientada a Objetos (POO), garantizando modularidad, encapsulamiento y alta cohesión:

1.  **Capa de Entidades (`src/entidades/`)**: Clases puras del dominio como `Deportista`, `Entrenamiento`, `Serie`, `Ritmo`, `Objetivo`, `PlanSemanal`, `MediaCorporal` y `RecordPersonal`. Implementan herencia y polimorfismo.
2.  **Capa de Servicios (`src/servicios/`)**: Controladores lógicos como `GestionAtletas` y `GestionEntrenamientos` que manejan la lógica de negocio y cálculos de rendimiento.
3.  **Capa de Persistencia (`src/persistencia/`)**: Manejo de datos mediante `manejador_archivos.py`, utilizando ficheros CSV y serialización binaria con Pickle para la preservación de objetos complejos.
4.  **Capa de Presentación / UI**: Interfaz gráfica moderna construida con la librería `customtkinter`.

### 🛡️ Sistema de Excepciones
El proyecto implementa una jerarquía completa de excepciones personalizadas para garantizar la estabilidad del software, siguiendo las convenciones del Tema 09 (PascalCase acabado en Exception):
* **Persistencia**: `PersistenciaException`, `ArchivoCorruptoException`.
* **Servicios**: `AtletaYaRegistradoException`, `CalculoImcException`, `SesionInvalidaException`.
* **Entidades**: `ValorFisicoInvalidoException`, `PlanSemanalIncoherenteException`.

---

## ⚙️ Guía de Instalación y Ejecución Detallada

Siga estos pasos exactamente para poner en marcha la aplicación. Se recomienda usar **Python 3.10** o superior.

### 🔹 Paso 1: Descarga del Proyecto
Descargue o clone el repositorio en una carpeta de su elección.

### 🔹 Paso 2: Ejecución en Windows (PowerShell)
1.  Abra el menú de inicio, escriba **PowerShell** y ábralo.
2.  Navegue hasta la carpeta del proyecto usando el comando `cd`:
    ```powershell
    cd C:\\ruta\\a\\la\\carpeta\\del\\proyecto
    ```
3.  Cree el entorno virtual para aislar las librerías:
    ```powershell
    python -m venv venv
    ```
4.  Active el entorno virtual:
    ```powershell
    .\\venv\\Scripts\\Activate.ps1
    ```
    *Si recibe un error de "políticas de ejecución", escriba: `Set-ExecutionPolicy Unrestricted -Scope CurrentUser` y pulse Enter.*
5.  Instale las librerías necesarias:
    ```powershell
    pip install -r requirements.txt
    ```
6.  Inicie la aplicación:
    ```powershell
    python main.py
    ```

### 🔹 Paso 3: Ejecución en Linux (Terminal)
1.  Abra su terminal favorita.
2.  Navegue hasta la carpeta del proyecto:
    ```bash
    cd /ruta/al/proyecto
    ```
3.  Cree el entorno virtual:
    ```bash
    python3 -m venv venv
    ```
4.  Active el entorno virtual:
    ```bash
    source venv/bin/activate
    ```
5.  Instale las librerías necesarias:
    ```bash
    pip install -r requirements.txt
    ```
6.  Inicie la aplicación:
    ```bash
    python3 main.py
    ```
### 🔹 Paso 4: Ejecutable
1.  Navegue hasta el ejecutable:
    ```bash
    cd /ruta/al/ejecutable
    ```
2. En Linux es necesario dar permisos de ejecución al fichero antes de abrirlo por primera vez. Esto es un requisito del sistema operativo Linux:
```bash
chmod +x dist/UAFitnessCoach
./dist/UAFitnessCoach
 ```
A partir de ese momento, el ejecutable puede abrirse directamente sin repetir el chmod +x.

---

## 🚀 Uso de la Aplicación
1.  **Directorio**: Registre nuevos atletas en la pestaña inicial. Se validará automáticamente que no haya nombres duplicados.
2.  **Expediente del Atleta**: Haga clic en "Gestionar Perfil" para acceder a:
    * **Planificación**: Horario semanal interactivo para definir rutinas.
    * **Diario de Cargas**: Registro de series (peso/repeticiones) que calcula el volumen de entreno.
    * **Biometría**: Gráficas automáticas de evolución de peso y grasa corporal.
3.  **Ranking**: Visualice quién lidera el rendimiento acumulado en base a los entrenamientos registrados.
4.  **Guardado**: Todos los datos se sincronizan automáticamente en ficheros binarios dentro de la carpeta `data/` al cerrar el programa.
"""