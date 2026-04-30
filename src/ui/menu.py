import customtkinter as ctk
from datetime import date


from src.servicios.gestion_atletas import GestionAtletas
from src.servicios.gestion_entrenamientos import GestionEntrenamientos
from src.entidades.entrenamiento import EntrenamientoFuerza, EntrenamientoCardio
from src.entidades.ritmo import Ritmo

# Configuración de apariencia
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MenuPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Inicialización de servicios
        self.atletismo = GestionAtletas()
        self.gym = GestionEntrenamientos()

        # Carga automática de datos al abrir
        self.atletismo.cargar_estado()
        self.gym.cargar_estado()

        # Configuración de la Ventana
        self.title("SISTEMA DE GESTIÓN DEPORTIVA")
        self.geometry("600x700")


        self.protocol("WM_DELETE_WINDOW", self.opcion_salir_y_guardar)

        # Título principal
        self.label_titulo = ctk.CTkLabel(self, text="--- LogiFit---", font=("Arial", 24, "bold"))
        self.label_titulo.pack(pady=20)


        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=10)

        self.tab1 = self.tabs.add("1. Registrar Atleta")
        self.tab2 = self.tabs.add("2. Registrar Entreno")
        self.tab3 = self.tabs.add("3. Ver Resumen")

        self.setup_opcion_1()
        self.setup_opcion_2()
        self.setup_opcion_3()

        # Botón de salida rápida
        self.btn_salir = ctk.CTkButton(self, text="Guardar y Salir (Opción 4)",
                                       fg_color="#CC0000", hover_color="#990000",
                                       command=self.opcion_salir_y_guardar)
        self.btn_salir.pack(pady=20)

    # ==========================================
    # OPCIÓN 1: REGISTRAR DEPORTISTA
    # ==========================================
    def setup_opcion_1(self):
        ctk.CTkLabel(self.tab1, text="Datos del nuevo atleta:", font=("Arial", 16)).pack(pady=10)

        self.ent_nombre = ctk.CTkEntry(self.tab1, placeholder_text="Nombre", width=250)
        self.ent_nombre.pack(pady=5)

        self.ent_peso = ctk.CTkEntry(self.tab1, placeholder_text="Peso (kg)", width=250)
        self.ent_peso.pack(pady=5)

        self.ent_altura = ctk.CTkEntry(self.tab1, placeholder_text="Altura (m)", width=250)
        self.ent_altura.pack(pady=5)

        ctk.CTkButton(self.tab1, text="Ejecutar Registro", command=self.ejecutar_opcion_1).pack(pady=20)
        self.res_opcion1 = ctk.CTkLabel(self.tab1, text="")
        self.res_opcion1.pack()

    def ejecutar_opcion_1(self):
        try:
            n = self.ent_nombre.get()
            p = float(self.ent_peso.get())
            a = float(self.ent_altura.get())
            self.atletismo.registrar_atleta(n, p, a)
            self.res_opcion1.configure(text=f"Atleta {n} registrado.", text_color="green")
            self.actualizar_resumen()
        except ValueError:
            self.res_opcion1.configure(text="Error en los datos", text_color="red")

    # ==========================================
    # OPCIÓN 2: REGISTRAR ENTRENAMIENTO
    # ==========================================
    def setup_opcion_2(self):
        ctk.CTkLabel(self.tab2, text="Tipo de entrenamiento:", font=("Arial", 16)).pack(pady=10)

        self.tipo_entreno = ctk.CTkOptionMenu(self.tab2, values=["Fuerza", "Cardio"], width=250)
        self.tipo_entreno.pack(pady=5)

        self.ent_duracion = ctk.CTkEntry(self.tab2, placeholder_text="Duración (min)", width=250)
        self.ent_duracion.pack(pady=5)

        self.ent_extra = ctk.CTkEntry(self.tab2, placeholder_text="Peso (kg) / Distancia (km)", width=250)
        self.ent_extra.pack(pady=5)

        ctk.CTkButton(self.tab2, text="Registrar Sesión", command=self.ejecutar_opcion_2).pack(pady=20)
        self.res_opcion2 = ctk.CTkLabel(self.tab2, text="")
        self.res_opcion2.pack()

    def ejecutar_opcion_2(self):
        try:
            tipo = self.tipo_entreno.get()
            dur = int(self.ent_duracion.get())
            val = float(self.ent_extra.get())
            fec = date.today().strftime("%Y-%m-%d")
            id_e = len(self.gym._historial_sesiones) + 100

            if tipo == "Fuerza":
                # Usamos vuestras clases originales
                entreno = EntrenamientoFuerza(fec, dur, val, 10, id_e)
            else:
                rit = Ritmo(5, 30)
                entreno = EntrenamientoCardio(fec, dur, val, rit, id_e)

            self.gym.registrar_entrenamiento(entreno)
            rend = entreno.calcular_rendimiento()
            self.res_opcion2.configure(text=f"Guardado. Rendimiento: {rend}", text_color="green")
        except:
            self.res_opcion2.configure(text="Error en los datos", text_color="red")

    # ==========================================
    # OPCIÓN 3: VER RESUMEN E IMC
    # ==========================================
    def setup_opcion_3(self):
        self.caja_resumen = ctk.CTkTextbox(self.tab3, width=500, height=350)
        self.caja_resumen.pack(pady=10, padx=10)

        ctk.CTkButton(self.tab3, text="Refrescar Lista", command=self.actualizar_resumen).pack(pady=5)
        self.actualizar_resumen()

    def actualizar_resumen(self):
        self.caja_resumen.delete("0.0", "end")
        self.caja_resumen.insert("end", "--- RESUMEN DE ESTADO ---\n\n")

        for a in self.atletismo.obtener_todos():
            imc = self.atletismo.calcular_imc_atleta(a)
            self.caja_resumen.insert("end", f"Atleta: {a._nombre}\nIMC: {imc}\n")
            self.caja_resumen.insert("end", "-" * 30 + "\n")

        self.caja_resumen.insert("end", f"\n{self.atletismo.obtener_resumen_atleta()}")

    # ==========================================
    # OPCIÓN 4: SALIR Y GUARDAR
    # ==========================================
    def opcion_salir_y_guardar(self):
        # Llamamos a vuestro manejador de archivos mediante los servicios
        self.atletismo.guardar_estado()
        self.gym.guardar_estado()
        print("Guardando datos y saliendo... ¡Buen entreno!")
        self.destroy()


if __name__ == "__main__":
    app = MenuPrincipal()
    app.mainloop()