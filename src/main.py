import customtkinter as ctk
from datetime import date

# Importación de la Capa de Servicios
from src.servicios.gestion_atletas import GestionAtletas

[cite: 10]
from src.servicios.gestion_entrenamientos import GestionEntrenamientos

[cite: 11]

# Importación de Entidades necesarias para la creación de objetos
from src.entidades.entrenamiento import EntrenamientoFuerza, EntrenamientoCardio

[cite: 3]
from src.entidades.ritmo import Ritmo

[cite: 8]

# --- CONFIGURACIÓN GLOBAL DE LA UI ---
ctk.set_appearance_mode("dark")  # Modo oscuro por defecto
ctk.set_default_color_theme("blue")  # Tema de color principal


class AppGestionDeportiva(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. Inicialización de Servicios y Carga de Persistencia
        self.atletismo = GestionAtletas()
        self.gym = GestionEntrenamientos()

        # Cargamos los datos guardados en los archivos .pkl al iniciar
        self.atletismo.cargar_estado()
        self.gym.cargar_estado()

        # 2. Configuración de la Ventana Principal
        self.title("Gestor de Rendimiento B5 - Universidad de Alicante")
        self.geometry("700x750")

        # Protocolo de cierre: Guarda datos automáticamente al pulsar la 'X'
        self.protocol("WM_DELETE_WINDOW", self.finalizar_y_guardar)

        # 3. Diseño de la Interfaz (Layout)
        self.label_header = ctk.CTkLabel(self, text="SISTEMA DE GESTIÓN DEPORTIVA", font=("Arial", 24, "bold"))
        self.label_header.pack(pady=20)

        # Sistema de Pestañas (Equivalente al Menú de Consola)
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=10)

        self.tab_atleta = self.tabs.add("👤 Registrar Atleta")
        self.tab_entreno = self.tabs.add("🏋️ Registrar Entreno")
        self.tab_resumen = self.tabs.add("📊 Resumen e IMC")

        # Configuración de cada sección
        self.crear_interfaz_atleta()
        self.crear_interfaz_entrenamiento()
        self.crear_interfaz_resumen()

    # ==========================================
    # SECCIÓN: REGISTRO DE ATLETAS (Opción 1)
    # ==========================================
    def crear_interfaz_atleta(self):
        ctk.CTkLabel(self.tab_atleta, text="Datos del Deportista", font=("Arial", 18, "bold")).pack(pady=15)

        self.entry_nom = ctk.CTkEntry(self.tab_atleta, placeholder_text="Nombre Completo", width=350)
        self.entry_nom.pack(pady=10)

        self.entry_peso = ctk.CTkEntry(self.tab_atleta, placeholder_text="Peso actual (kg)", width=350)
        self.entry_peso.pack(pady=10)

        self.entry_alt = ctk.CTkEntry(self.tab_atleta, placeholder_text="Altura (m) - Ejemplo: 1.75", width=350)
        self.entry_alt.pack(pady=10)

        ctk.CTkButton(self.tab_atleta, text="Registrar en Sistema", command=self.ui_registrar_atleta).pack(pady=20)

        self.lbl_status_atleta = ctk.CTkLabel(self.tab_atleta, text="")
        self.lbl_status_atleta.pack()

    def ui_registrar_atleta(self):
        try:
            nombre = self.entry_nom.get()
            peso = float(self.entry_peso.get())
            altura = float(self.entry_alt.get())

            # Llamada al servicio de atletas
            self.atletismo.registrar_atleta(nombre, peso, altura)

            self.lbl_status_atleta.configure(text=f"✅ Atleta {nombre} registrado con éxito", text_color="green")
            self.limpiar_campos_atleta()
            self.ui_actualizar_resumen()
        except ValueError:
            self.lbl_status_atleta.configure(text="❌ Error: Introduce valores numéricos válidos", text_color="red")

    def limpiar_campos_atleta(self):
        self.entry_nom.delete(0, 'end')
        self.entry_peso.delete(0, 'end')
        self.entry_alt.delete(0, 'end')

    # ==========================================
    # SECCIÓN: REGISTRO DE ENTRENOS (Opción 2)
    # ==========================================
    def crear_interfaz_entrenamiento(self):
        ctk.CTkLabel(self.tab_entreno, text="Nueva Sesión de Entrenamiento", font=("Arial", 18, "bold")).pack(pady=10)

        # Duración común
        self.entry_dur = ctk.CTkEntry(self.tab_entreno, placeholder_text="Duración (minutos)", width=350)
        self.entry_dur.pack(pady=10)

        # Selector de Tipo (Fuerza o Cardio)
        self.tipo_entreno_var = ctk.StringVar(value="Fuerza")
        self.menu_tipo = ctk.CTkOptionMenu(self.tab_entreno, values=["Fuerza", "Cardio"],
                                           variable=self.tipo_entreno_var,
                                           command=self.ui_alternar_campos_entreno, width=350)
        self.menu_tipo.pack(pady=10)

        # Frames para campos específicos
        self.frame_fuerza = ctk.CTkFrame(self.tab_entreno, fg_color="transparent")
        self.ent_peso_f = ctk.CTkEntry(self.frame_fuerza, placeholder_text="Peso total levantado (kg)", width=350)
        self.ent_peso_f.pack(pady=5)
        self.ent_reps_f = ctk.CTkEntry(self.frame_fuerza, placeholder_text="Repeticiones totales", width=350)
        self.ent_reps_f.pack(pady=5)

        self.frame_cardio = ctk.CTkFrame(self.tab_entreno, fg_color="transparent")
        self.ent_dist_c = ctk.CTkEntry(self.frame_cardio, placeholder_text="Distancia total (km)", width=350)
        self.ent_dist_c.pack(pady=5)

        # Inicialmente mostramos Fuerza
        self.frame_fuerza.pack()

        ctk.CTkButton(self.tab_entreno, text="Guardar Entrenamiento", command=self.ui_registrar_entreno).pack(pady=20)
        self.lbl_status_entreno = ctk.CTkLabel(self.tab_entreno, text="")
        self.lbl_status_entreno.pack()

    def ui_alternar_campos_entreno(self, seleccion):
        if seleccion == "Fuerza":
            self.frame_cardio.pack_forget()
            self.frame_fuerza.pack()
        else:
            self.frame_fuerza.pack_forget()
            self.frame_cardio.pack()

    def ui_registrar_entreno(self):
        try:
            tipo = self.tipo_entreno_var.get()
            fecha = date.today().strftime("%Y-%m-%d")
            duracion = int(self.entry_dur.get())
            id_e = len(self.gym._historial_sesiones) + 100

            if tipo == "Fuerza":
                peso_l = float(self.ent_peso_f.get())
                reps = int(self.ent_reps_f.get())
                # Polimorfismo: Creamos objeto de Fuerza
                entreno = EntrenamientoFuerza(fecha, duracion, peso_l, reps, id_e)
            else:
                dist = float(self.ent_dist_c.get())
                ritmo = Ritmo(5, 45)  # Ritmo genérico para la prueba
                # Polimorfismo: Creamos objeto de Cardio
                entreno = EntrenamientoCardio(fecha, duracion, dist, ritmo, id_e)

            self.gym.registrar_entrenamiento(entreno)
            rend = entreno.calcular_rendimiento()

            self.lbl_status_entreno.configure(text=f"✅ Guardado. Rendimiento: {rend}", text_color="green")
        except ValueError:
            self.lbl_status_entreno.configure(text="❌ Error: Verifica los datos numéricos", text_color="red")

    # ==========================================
    # SECCIÓN: RESUMEN E IMC (Opción 3)
    # ==========================================
    def crear_interfaz_resumen(self):
        self.txt_resumen = ctk.CTkTextbox(self.tab_resumen, width=550, height=400, font=("Consolas", 13))
        self.txt_resumen.pack(pady=20, padx=20)

        ctk.CTkButton(self.tab_resumen, text="Actualizar Listado", command=self.ui_actualizar_resumen).pack(pady=10)
        self.ui_actualizar_resumen()

    def ui_actualizar_resumen(self):
        self.txt_resumen.delete("0.0", "end")
        self.txt_resumen.insert("end", "--- RESUMEN DE PROGRESO DE ATLETAS ---\n\n")

        atletas = self.atletismo.obtener_todos()
        if not atletas:
            self.txt_resumen.insert("end", "No hay atletas registrados actualmente.")
        else:
            for a in atletas:
                imc = self.atletismo.calcular_imc_atleta(a)
                self.txt_resumen.insert("end", f"👤 Atleta: {a._nombre}\n")
                self.txt_resumen.insert("end", f"   Peso: {a._peso}kg | IMC: {imc}\n")
                self.txt_resumen.insert("end", "-" * 40 + "\n")

            self.txt_resumen.insert("end", f"\n{self.atletismo.obtener_resumen_atleta()}")

    # ==========================================
    # CIERRE Y PERSISTENCIA (Opción 4)
    # ==========================================
    def finalizar_y_guardar(self):
        """Método para asegurar que los datos se guardan antes de salir[cite: 13, 14]"""
        print("Persistiendo datos en disco...")
        self.atletismo.guardar_estado()
        self.gym.guardar_estado()
        self.destroy()


if __name__ == "__main__":
    app = AppGestionDeportiva()
    app.mainloop()