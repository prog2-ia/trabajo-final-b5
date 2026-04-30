import customtkinter as ctk
from datetime import date
from tkinter import messagebox

# Importación de arquitectura de capas
from src.servicios.gestion_atletas import GestionAtletas
from src.servicios.gestion_entrenamientos import GestionEntrenamientos
from src.entidades.entrenamiento import EntrenamientoFuerza, EntrenamientoCardio
from src.entidades.plansemanal import PlanSemanal
from src.entidades.serie import Serie
from src.entidades.ritmo import Ritmo
from src.entidades.objetivo import Objetivo
from src.entidades.mediapersonal import MediaCorporal
from src.entidades.recordpersonal import RecordPersonal


class AppFitnessPro_UA(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Servicios
        self.atletismo = GestionAtletas()
        self.gym = GestionEntrenamientos()
        self.atletismo.cargar_estado()
        self.gym.cargar_estado()

        self.title("UA Fitness Management System - Grupo B5")
        self.geometry("1400x950")
        self.atleta_actual = None

        # Layout Principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._setup_sidebar()
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)

        self.navegar("directorio")

    def _setup_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(sidebar, text="UA FITNESS PRO", font=("Impact", 28)).pack(pady=40)

        ctk.CTkButton(sidebar, text="👥 Directorio General", command=lambda: self.navegar("directorio")).pack(pady=10,
                                                                                                             padx=20,
                                                                                                             fill="x")
        ctk.CTkButton(sidebar, text="🏆 Ranking de Élite", fg_color="#D4AC0D", text_color="black",
                      command=lambda: self.navegar("ranking")).pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(sidebar, text="📥 Sincronizar Datos", fg_color="#2E4053", command=self.guardar_datos).pack(
            side="bottom", pady=30, padx=20, fill="x")

    def navegar(self, vista):
        for widget in self.main_container.winfo_children(): widget.destroy()
        if vista == "directorio":
            self.render_directorio()
        elif vista == "expediente":
            self.render_expediente()
        elif vista == "ranking":
            self.render_ranking()

    # ==========================================
    # 1. DIRECTORIO (LISTA DE ATLETAS)
    # ==========================================
    def render_directorio(self):
        ctk.CTkLabel(self.main_container, text="CENTRO DE MANDO DE DEPORTISTAS", font=("Arial", 24, "bold")).pack(
            pady=15)

        f_alta = ctk.CTkFrame(self.main_container)
        f_alta.pack(fill="x", pady=10)
        self.ent_n = ctk.CTkEntry(f_alta, placeholder_text="Nombre del nuevo prospecto...", width=300)
        self.ent_n.pack(side="left", padx=20, pady=20)
        ctk.CTkButton(f_alta, text="Registrar en la Academia", command=self.registrar_atleta).pack(side="left")

        scroll = ctk.CTkScrollableFrame(self.main_container, label_text="Atletas Bajo Supervisión")
        scroll.pack(fill="both", expand=True, pady=10)

        for a in self.atletismo.obtener_todos():
            card = ctk.CTkFrame(scroll, border_width=1, border_color="#34495E")
            card.pack(fill="x", padx=15, pady=8)
            ctk.CTkLabel(card, text=f"DEPORTISTA: {a._nombre.upper()}", font=("Arial", 14, "bold")).pack(side="left",
                                                                                                         padx=30,
                                                                                                         pady=20)

            ctk.CTkButton(card, text="Gestionar Perfil", fg_color="#2980B9",
                          command=lambda obj=a: self.abrir_expediente(obj)).pack(side="right", padx=10)
            ctk.CTkButton(card, text="🗑️", width=45, fg_color="#922B21",
                          command=lambda obj=a: self.eliminar_atleta(obj)).pack(side="right")

    # ==========================================
    # 2. EXPEDIENTE (PERFIL 360º)
    # ==========================================
    def render_expediente(self):
        a = self.atleta_actual
        ctk.CTkButton(self.main_container, text="← Volver al Centro de Mando", width=120,
                      command=lambda: self.navegar("directorio")).pack(anchor="w")

        # --- HEADER DEL EXPEDIENTE ---
        header = ctk.CTkFrame(self.main_container, fg_color="#17202A", corner_radius=15)
        header.pack(fill="x", pady=20)

        ctk.CTkLabel(header, text=f"EXPEDIENTE TÉCNICO: {a._nombre}", font=("Arial", 28, "bold")).pack(side="left",
                                                                                                       padx=30, pady=25)

        stats_frame = ctk.CTkFrame(header, fg_color="transparent")
        stats_frame.pack(side="right", padx=30)

        # Info rápida basada en lógica de Atleta
        ctk.CTkLabel(stats_frame, text=f"IMC: {self.atletismo.calcular_imc_atleta(a)}", font=("Arial", 16, "bold"),
                     text_color="#27AE60").pack(side="left", padx=15)
        ctk.CTkLabel(stats_frame, text=f"Peso Inicial: {a._peso}kg", font=("Arial", 12)).pack(side="left", padx=15)

        # --- TABS DE FUNCIONALIDADES ---
        tabs = ctk.CTkTabview(self.main_container)
        tabs.pack(fill="both", expand=True)

        t_plan = tabs.add("📅 Planificación")
        t_logs = tabs.add("🏋️ Diario de Cargas")
        t_body = tabs.add("📏 Biometría")
        t_goals = tabs.add("🎯 Récords y Metas")

        self._build_planificador(t_plan)
        self._build_diario(t_logs)
        self._build_biometria(t_body)
        self._build_objetivos(t_goals)

    # --- SUB-MÓDULO: PLANIFICADOR SEMANAL ---
    def _build_planificador(self, parent):
        ctk.CTkLabel(parent, text="MATRIZ DE ENTRENAMIENTO SEMANAL", font=("Arial", 16, "bold")).pack(pady=15)
        grid = ctk.CTkFrame(parent, fg_color="transparent")
        grid.pack(pady=10)

        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        self.controles_plan = {}

        for i, dia in enumerate(dias):
            col = ctk.CTkFrame(grid, width=160, height=220, border_width=1, border_color="#5D6D7E")
            col.grid(row=0, column=i, padx=5)
            col.grid_propagate(False)

            ctk.CTkLabel(col, text=dia, font=("Arial", 13, "bold"), text_color="#AED6F1").pack(pady=10)

            sel = ctk.CTkOptionMenu(col, values=["DESCANSO", "FUERZA", "CARDIO", "HIIT", "MOVILIDAD"], width=130)
            sel.pack(pady=20)
            self.controles_plan[dia] = sel

        ctk.CTkButton(parent, text="Sincronizar Calendario de Atleta", fg_color="#1E8449",
                      command=self.guardar_horario).pack(pady=30)

    # --- SUB-MÓDULO: DIARIO DE CARGAS ---
    def _build_diario(self, parent):
        f_registro = ctk.CTkFrame(parent)
        f_registro.pack(fill="x", padx=30, pady=20)

        ctk.CTkLabel(f_registro, text="Registrar Nueva Serie (Capa de Ejecución)", font=("Arial", 15, "bold")).grid(
            row=0, column=0, columnspan=2, pady=10)
        self.e_reps = ctk.CTkEntry(f_registro, placeholder_text="Repeticiones");
        self.e_reps.grid(row=1, column=0, padx=15, pady=10)
        self.e_kg = ctk.CTkEntry(f_registro, placeholder_text="Carga en kg");
        self.e_kg.grid(row=1, column=1, padx=15, pady=10)

        ctk.CTkButton(f_registro, text="Procesar Serie", command=self.log_serie).grid(row=2, column=0, columnspan=2,
                                                                                      pady=20)

    # --- SUB-MÓDULO: BIOMETRÍA (MediaCorporal) ---
    def _build_biometria(self, parent):
        f_med = ctk.CTkFrame(parent)
        f_med.pack(fill="x", padx=30, pady=20)

        ctk.CTkLabel(f_med, text="Nueva Evolución Corporal", font=("Arial", 15, "bold")).pack(pady=10)
        self.e_grasa = ctk.CTkEntry(f_med, placeholder_text="% Grasa Corporal");
        self.e_grasa.pack(pady=5)
        self.e_peso_act = ctk.CTkEntry(f_med, placeholder_text="Peso Actual (kg)");
        self.e_peso_act.pack(pady=5)

        ctk.CTkButton(f_med, text="Registrar Evolución", command=self.log_biometria).pack(pady=15)

    # --- SUB-MÓDULO: METAS Y PRs ---
    def _build_objetivos(self, parent):
        # Objetivos
        f_meta = ctk.CTkFrame(parent)
        f_meta.pack(fill="x", padx=30, pady=10)
        ctk.CTkLabel(f_meta, text="Fijar Meta de Rendimiento", font=("Arial", 14, "bold")).pack(pady=5)
        self.e_meta_t = ctk.CTkEntry(f_meta, placeholder_text="Tipo (ej: Fuerza)");
        self.e_meta_t.pack(side="left", padx=20, pady=10)
        self.e_meta_v = ctk.CTkEntry(f_meta, placeholder_text="Valor Objetivo");
        self.e_meta_v.pack(side="left", padx=10)
        ctk.CTkButton(f_meta, text="Fijar Meta", command=self.log_meta).pack(side="left", padx=10)

    # ==========================================
    # 3. RANKING (LEADERBOARD DE RENDIMIENTO)
    # ==========================================
    def render_ranking(self):
        ctk.CTkLabel(self.main_container, text="🏆 RANKING DE RENDIMIENTO ACUMULADO", font=("Impact", 35)).pack(pady=30)

        # Lógica: Suma de rendimientos calculados en Entrenamiento
        ranking = []
        for a in self.atletismo.obtener_todos():
            total = sum(s.calcular_rendimiento() for s in self.gym._historial_sesiones)
            ranking.append((a._nombre, total))

        ranking.sort(key=lambda x: x[1], reverse=True)

        for pos, (nombre, puntos) in enumerate(ranking, 1):
            f = ctk.CTkFrame(self.main_container, border_width=1, fg_color="#D4AC0D" if pos == 1 else "transparent")
            f.pack(fill="x", padx=120, pady=6)

            ctk.CTkLabel(f, text=f"{pos}. {nombre.upper()}", font=("Arial", 18, "bold"),
                         text_color="black" if pos == 1 else "white").pack(side="left", padx=40, pady=15)
            ctk.CTkLabel(f, text=f"Puntaje de Élite: {puntos:.1f}", font=("Consolas", 16),
                         text_color="black" if pos == 1 else "white").pack(side="right", padx=40)

    # --- CONTROLADORES ---

    def registrar_atleta(self):
        if self.ent_n.get():
            self.atletismo.registrar_atleta(self.ent_n.get(), 80.0, 1.80)
            self.render_directorio()

    def abrir_expediente(self, atleta):
        self.atleta_actual = atleta
        self.navegar("expediente")

    def log_serie(self):
        try:
            s = Serie(int(self.e_reps.get()), float(self.e_kg.get()))
            vol = s.repeticiones * s._peso
            ent = EntrenamientoFuerza(date.today().strftime("%Y-%m-%d"), 60, vol, int(self.e_reps.get()), 1)
            self.gym.registrar_entrenamiento(ent)
            messagebox.showinfo("Capa de Datos", "Serie integrada en el historial del atleta.")
        except:
            pass

    def log_biometria(self):
        m = MediaCorporal(date.today().strftime("%d/%m/%Y"), float(self.e_grasa.get()), float(self.e_peso_act.get()))
        self.atletismo.añadir_medida(m)
        messagebox.showinfo("Biometría", "Composición corporal actualizada.")

    def log_meta(self):
        o = Objetivo(self.e_meta_t.get(), float(self.e_meta_v.get()), date.today())
        self.atletismo.fijar_objetivo(o)

    def guardar_horario(self):
        dias = list(self.controles_plan.keys())
        rutinas = [c.get() for c in self.controles_plan.values()]
        self.gym.programar_semana(dias, rutinas)
        messagebox.showinfo("Calendario", f"Horario de alto rendimiento sincronizado para {self.atleta_actual._nombre}")

    def eliminar_atleta(self, atleta):
        if atleta in self.atletismo._atletas:
            self.atletismo._atletas.remove(atleta)
            self.render_directorio()

    def guardar_datos(self):
        self.atletismo.guardar_estado();
        self.gym.guardar_estado()
        messagebox.showinfo("Persistencia", "Toda la información ha sido salvada en archivos binarios.")


if __name__ == "__main__":
    AppFitnessPro_UA().mainloop()