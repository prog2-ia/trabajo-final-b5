"""
UA Fitness Coach - Interfaz completa y útil
Rediseño completo con gráficas, ranking, calendario semanal y récords.
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import date, timedelta
import tkinter as tk
import os
import sys

# Importación de Servicios
from src.servicios.gestion_atletas import GestionAtletas
from src.servicios.gestion_entrenamientos import GestionEntrenamientos

# Importación de Entidades
from src.entidades.entrenamiento import EntrenamientoFuerza, EntrenamientoCardio
from src.entidades.objetivo import Objetivo
from src.entidades.mediapersonal import MediaCorporal
from src.entidades.recordpersonal import RecordPersonal
from src.entidades.ejercicio import Ejercicio

# Importación de Excepciones y Persistencia
from src.entidades.excepciones_entidades import EntidadException
from src.servicios.excepciones_servicios import ServicioException
from src.persistencia.excepciones_persistencia import FitnessAppException, PersistenciaException
from src.persistencia.manejador_archivos import ManejadorArchivos

# Matplotlib para gráficas embebidas en tkinter
try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_OK = True
except ImportError:
    MATPLOTLIB_OK = False

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ─────────────────────────────────────────────
# PALETA DE COLORES GLOBAL
# ─────────────────────────────────────────────
C_AZUL = "#00A3FF"
C_VERDE = "#27AE60"
C_ROJO = "#C0392B"
C_AMARILLO = "#F39C12"
C_FONDO = "#0D1B2A"
C_CARD = "#1B2A3B"
C_CARD2 = "#162032"
C_TEXTO = "#ECF0F1"
C_MUTED = "#7F8C8D"

# ─────────────────────────────────────────────
# DATOS DE MUESTRA (para que la app se vea útil desde el primer uso)
# ─────────────────────────────────────────────
DATOS_MUESTRA = {
    "Carlos Martínez": {
        "peso": 82.0, "altura": 1.78,
        "biometria": [
            ("2024-10-01", 22.0, 83.0), ("2024-11-01", 20.5, 82.0),
            ("2024-12-01", 19.2, 81.5), ("2025-01-01", 18.0, 81.0),
            ("2025-02-01", 17.1, 80.5), ("2025-03-01", 16.5, 80.0),
        ],
        "objetivos": [
            ("Bajar grasa", 15.0, date.today() + timedelta(days=60)),
            ("Press banca 100kg", 100.0, date.today() + timedelta(days=120)),
        ],
        "sesiones_fuerza": [
            ("2025-01-10", 60, 80.0, 5, "Pecho"), ("2025-01-17", 60, 82.5, 5, "Pecho"),
            ("2025-01-24", 65, 85.0, 5, "Pecho"), ("2025-02-01", 65, 87.5, 4, "Pecho"),
            ("2025-02-08", 70, 90.0, 4, "Pecho"), ("2025-02-15", 70, 92.5, 4, "Pecho"),
            ("2025-01-12", 55, 100.0, 5, "Piernas"), ("2025-01-26", 55, 105.0, 5, "Piernas"),
            ("2025-02-09", 60, 110.0, 5, "Piernas"), ("2025-02-23", 60, 115.0, 4, "Piernas"),
        ],
        "sesiones_cardio": [
            ("2025-01-05", 30, 5.0, 6, 10), ("2025-01-12", 35, 6.0, 5, 55),
            ("2025-01-19", 30, 5.5, 5, 50), ("2025-02-02", 40, 7.0, 5, 45),
        ],
        "records": {"Press Banca": 92.5, "Sentadilla": 115.0, "Peso Muerto": 130.0},
        "plan": {"Lunes": "Pecho/Tríceps", "Martes": "Cardio 6km", "Miércoles": "Espalda/Bíceps",
                 "Jueves": "Descanso", "Viernes": "Piernas", "Sábado": "Cardio 8km", "Domingo": "Descanso"},
    },
    "Laura Sánchez": {
        "peso": 63.0, "altura": 1.65,
        "biometria": [
            ("2024-10-01", 26.0, 64.0), ("2024-11-01", 25.0, 63.5),
            ("2024-12-01", 24.2, 63.0), ("2025-01-01", 23.5, 62.5),
            ("2025-02-01", 22.8, 62.0), ("2025-03-01", 22.0, 61.5),
        ],
        "objetivos": [
            ("Correr 10K", 10.0, date.today() + timedelta(days=45)),
            ("Flexibilidad", 90.0, date.today() + timedelta(days=90)),
        ],
        "sesiones_fuerza": [
            ("2025-01-08", 50, 40.0, 8, "Glúteos"), ("2025-01-15", 50, 42.5, 8, "Glúteos"),
            ("2025-01-22", 55, 45.0, 8, "Glúteos"), ("2025-02-05", 55, 47.5, 6, "Glúteos"),
            ("2025-02-12", 60, 50.0, 6, "Glúteos"),
        ],
        "sesiones_cardio": [
            ("2025-01-06", 40, 5.5, 7, 20), ("2025-01-13", 42, 6.0, 7, 10),
            ("2025-01-20", 45, 6.5, 7, 0), ("2025-02-03", 48, 7.0, 6, 50),
            ("2025-02-10", 50, 7.5, 6, 40), ("2025-02-17", 52, 8.0, 6, 30),
        ],
        "records": {"Sentadilla Búlgara": 47.5, "Hip Thrust": 80.0, "Zancadas": 25.0},
        "plan": {"Lunes": "Glúteos/Core", "Martes": "Cardio 6km", "Miércoles": "Descanso",
                 "Jueves": "Full Body", "Viernes": "Cardio 8km", "Sábado": "Yoga/Flex", "Domingo": "Descanso"},
    },
    "Marcos Ruiz": {
        "peso": 91.0, "altura": 1.83,
        "biometria": [
            ("2024-10-01", 18.0, 92.0), ("2024-11-01", 17.5, 91.5),
            ("2024-12-01", 17.0, 91.0), ("2025-01-01", 16.8, 91.5),
            ("2025-02-01", 16.5, 92.0), ("2025-03-01", 16.0, 92.5),
        ],
        "objetivos": [("Peso Muerto 200kg", 200.0, date.today() + timedelta(days=180))],
        "sesiones_fuerza": [
            ("2025-01-07", 75, 160.0, 3, "Espalda"), ("2025-01-14", 75, 165.0, 3, "Espalda"),
            ("2025-01-21", 80, 170.0, 3, "Espalda"), ("2025-02-04", 80, 175.0, 3, "Espalda"),
            ("2025-02-11", 85, 180.0, 2, "Espalda"), ("2025-02-18", 85, 185.0, 2, "Espalda"),
            ("2025-01-09", 60, 120.0, 5, "Pecho"), ("2025-01-23", 65, 125.0, 4, "Pecho"),
            ("2025-02-06", 65, 127.5, 4, "Pecho"),
        ],
        "sesiones_cardio": [
            ("2025-01-10", 20, 3.0, 7, 0), ("2025-01-24", 20, 3.2, 6, 50),
        ],
        "records": {"Peso Muerto": 185.0, "Press Banca": 127.5, "Sentadilla": 150.0},
        "plan": {"Lunes": "Espalda/Bíceps", "Martes": "Descanso", "Miércoles": "Pecho/Tríceps",
                 "Jueves": "Piernas", "Viernes": "Hombros", "Sábado": "Cardio suave", "Domingo": "Descanso"},
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# CLASE PRINCIPAL DE LA APLICACIÓN
# ─────────────────────────────────────────────────────────────────────────────
class UAFitnessCoachApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.atletismo = GestionAtletas()
        self.gym = GestionEntrenamientos()
        self.atleta_actual = None
        self._datos_extra: dict = {}

        self.dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        dias_es = {"monday":"Lunes","tuesday":"Martes","wednesday":"Miércoles",
                   "thursday":"Jueves","friday":"Viernes","saturday":"Sábado","sunday":"Domingo"}
        hoy_real = dias_es.get(date.today().strftime("%A").lower(), "Lunes")
        self.dia_simulado_var = ctk.StringVar(value=hoy_real)

        try:
            self.atletismo.cargar_estado()
            self.gym.cargar_estado()
            extra = ManejadorArchivos.cargar_binario("data/extra_data.pkl")
            if extra:
                self._datos_extra = extra
        except PersistenciaException:
            pass
        except FitnessAppException as e:
            messagebox.showerror("Error de datos", str(e))

        if not self.atletismo.obtener_todos():
            self._cargar_datos_muestra()

        self.title("UA Fitness Coach • Dashboard")
        self.geometry("1280x820")
        self.minsize(1100, 700)
        self.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        self.configure(fg_color=C_FONDO)

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)

        self.mostrar_bienvenida()

    def _al_cambiar_dia(self, valor):
        if self.atleta_actual:
            self.mostrar_perfil(self.atleta_actual)
        else:
            self.mostrar_dashboard()

    # ─────────────────────────────────────────
    # DATOS DE MUESTRA
    # ─────────────────────────────────────────
    def _cargar_datos_muestra(self):
        for nombre, datos in DATOS_MUESTRA.items():
            try:
                a = self.atletismo.registrar_atleta(nombre, datos["peso"], datos["altura"])
            except ServicioException:
                continue

            self._datos_extra[nombre] = {
                "biometria": datos["biometria"],
                "sesiones_fuerza": datos["sesiones_fuerza"],
                "sesiones_cardio": datos["sesiones_cardio"],
                "records": datos["records"],
                "plan": datos["plan"],
                "objetivos": datos["objetivos"],
            }

    def _get_extra(self, nombre: str) -> dict:
        if nombre not in self._datos_extra:
            self._datos_extra[nombre] = {
                "biometria": [], "sesiones_fuerza": [],
                "sesiones_cardio": [], "records": {},
                "plan": {d: "Descanso" for d in self.dias_semana},
                "objetivos": [],
            }
        return self._datos_extra[nombre]

    # ─────────────────────────────────────────
    # UTILIDADES DE INTERFAZ
    # ─────────────────────────────────────────
    def limpiar_pantalla(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

    def _header(self, parent, titulo: str, boton_volver=None) -> ctk.CTkFrame:
        h = ctk.CTkFrame(parent, fg_color=C_CARD2, height=68, corner_radius=0)
        h.pack(fill="x")
        h.pack_propagate(False)
        inner = ctk.CTkFrame(h, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20)

        if boton_volver:
            ctk.CTkButton(inner, text="← Volver", width=90, height=34,
                          fg_color=C_CARD, hover_color="#263547",
                          command=boton_volver).pack(side="left", pady=17)

        ctk.CTkLabel(inner, text=titulo, font=("Arial", 22, "bold"), text_color=C_AZUL).pack(side="left", padx=16, pady=17)
        return h

    def _card(self, parent, **kwargs) -> ctk.CTkFrame:
        defaults = dict(fg_color=C_CARD, corner_radius=12, border_width=1, border_color="#263547")
        defaults.update(kwargs)
        return ctk.CTkFrame(parent, **defaults)

    def _label_titulo(self, parent, texto, **kwargs):
        defaults = dict(font=("Arial", 15, "bold"), text_color=C_TEXTO)
        defaults.update(kwargs)
        return ctk.CTkLabel(parent, text=texto, **defaults)

    def _label_muted(self, parent, texto, **kwargs):
        defaults = dict(font=("Arial", 12), text_color=C_MUTED)
        defaults.update(kwargs)
        return ctk.CTkLabel(parent, text=texto, **defaults)

    def _btn(self, parent, texto, comando, color=C_AZUL, **kwargs):
        return ctk.CTkButton(parent, text=texto, command=comando,
                             fg_color=color, hover_color=self._oscurecer(color),
                             corner_radius=8, **kwargs)

    @staticmethod
    def _oscurecer(hex_color: str) -> str:
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        factor = 0.75
        return f"#{int(r*factor):02x}{int(g*factor):02x}{int(b*factor):02x}"

    # ─────────────────────────────────────────
    # PANTALLA 1: BIENVENIDA
    # ─────────────────────────────────────────
    def mostrar_bienvenida(self):
        self.limpiar_pantalla()
        f = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        f.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(f, text="UA FITNESS", font=("Impact", 88), text_color=C_AZUL).pack(pady=5)
        ctk.CTkLabel(f, text="Professional Coaching Suite", font=("Arial", 22), text_color=C_MUTED).pack()

        n_atletas = len(self.atletismo.obtener_todos())
        ctk.CTkLabel(f, text=f"{n_atletas} atletas registrados", font=("Arial", 14), text_color=C_MUTED).pack(pady=6)

        self._btn(f, " ENTRAR AL SISTEMA ", self.mostrar_dashboard,
                  width=300, height=58, font=("Arial", 18, "bold")).pack(pady=30)

    # ─────────────────────────────────────────
    # PANTALLA 2: DASHBOARD DE ATLETAS (FIX BOTONES)
    # ─────────────────────────────────────────
    def mostrar_dashboard(self):
        self.limpiar_pantalla()
        h = self._header(self.main_frame, " Panel de Atletas")

        # FIX: Empacamos los botones dentro del inner_frame de h para que no se oculten
        inner_frame = h.winfo_children()[0]
        btn_row = ctk.CTkFrame(inner_frame, fg_color="transparent")
        btn_row.pack(side="right", padx=20)

        self._btn(btn_row, "+ Añadir Atleta", self.modal_añadir_alumno, color=C_VERDE, width=140).pack(side="left", padx=6)
        self._btn(btn_row, "✕ Eliminar Atleta", self.modal_eliminar_alumno, color=C_ROJO, width=140).pack(side="left", padx=6)
        self._btn(btn_row, " Ranking Global", self.mostrar_ranking_global, color="#8E44AD", width=140).pack(side="left", padx=6)
        self._btn(btn_row, " Guardar y Salir", self.cerrar_aplicacion, color=C_CARD, width=140).pack(side="left", padx=6)

        scroll = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=24, pady=20)
        self._grid_scroll = scroll
        self._renderizar_tarjetas()

    def _renderizar_tarjetas(self):
        for w in self._grid_scroll.winfo_children():
            w.destroy()

        atletas = self.atletismo.obtener_todos()
        if not atletas:
            ctk.CTkLabel(self._grid_scroll, text="No hay atletas. Añade uno con el botón de arriba.",
                         font=("Arial", 16), text_color=C_MUTED).pack(pady=60)
            return

        for i, atleta in enumerate(atletas):
            row, col = divmod(i, 4)
            datos = self._get_extra(atleta._nombre)

            card = self._card(self._grid_scroll, width=270, height=240)
            card.grid(row=row, column=col, padx=14, pady=14)
            card.grid_propagate(False)

            try:
                imc = self.atletismo.calcular_imc_atleta(atleta)
                if imc < 18.5: imc_color, imc_texto = "#3498DB", "Bajo peso"
                elif imc < 25.0: imc_color, imc_texto = C_VERDE, "Normal"
                elif imc < 30.0: imc_color, imc_texto = C_AMARILLO,"Sobrepeso"
                else: imc_color, imc_texto = C_ROJO, "Obesidad"
            except Exception:
                imc, imc_color, imc_texto = "—", C_MUTED, ""

            ctk.CTkLabel(card, text=atleta._nombre.upper(), font=("Arial", 16, "bold"), text_color=C_AZUL, wraplength=240).pack(pady=(18, 4))

            stats_frame = ctk.CTkFrame(card, fg_color="transparent")
            stats_frame.pack()
            ctk.CTkLabel(stats_frame, text=f"⚖ {atleta.peso} kg", font=("Arial", 13), text_color=C_TEXTO).grid(row=0, column=0, padx=10)
            ctk.CTkLabel(stats_frame, text=f"📏 {atleta._altura} m", font=("Arial", 13), text_color=C_TEXTO).grid(row=0, column=1, padx=10)

            badge = ctk.CTkFrame(card, fg_color=imc_color, corner_radius=8, height=28)
            badge.pack(pady=6, padx=20, fill="x")
            badge.pack_propagate(False)
            ctk.CTkLabel(badge, text=f"IMC {imc} • {imc_texto}", font=("Arial", 12, "bold"), text_color="white").pack(expand=True)

            n_sesiones = len(datos["sesiones_fuerza"]) + len(datos["sesiones_cardio"])
            n_records = len(datos["records"])
            ctk.CTkLabel(card, text=f"🏋 {n_sesiones} sesiones | 🏅 {n_records} récords", font=("Arial", 11), text_color=C_MUTED).pack(pady=2)

            self._btn(card, "Abrir Perfil →", lambda a=atleta: self.mostrar_perfil(a), color=C_AZUL, height=34).pack(side="bottom", pady=14, padx=20, fill="x")

    # ─────────────────────────────────────────
    # PANTALLA 3: PERFIL DEL ATLETA
    # ─────────────────────────────────────────
    def mostrar_perfil(self, atleta):
        self.limpiar_pantalla()
        self.atleta_actual = atleta
        datos = self._get_extra(atleta._nombre)

        self._header(self.main_frame, f" {atleta._nombre.upper()} — Panel de Control", boton_volver=self.mostrar_dashboard)

        bar = ctk.CTkFrame(self.main_frame, fg_color=C_CARD2, height=46, corner_radius=0)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        ctk.CTkLabel(bar, text="Cambiar atleta:", font=("Arial", 12), text_color=C_MUTED).pack(side="left", padx=(16, 8), pady=12)
        for a in self.atletismo.obtener_todos():
            color = C_AZUL if a._nombre == atleta._nombre else C_CARD
            btn = ctk.CTkButton(bar, text=a._nombre, fg_color=color, hover_color=self._oscurecer(C_AZUL), height=30, corner_radius=6, command=lambda x=a: self.mostrar_perfil(x))
            btn.pack(side="left", padx=4, pady=8)

        tabs = ctk.CTkTabview(self.main_frame, fg_color=C_FONDO, segmented_button_fg_color=C_CARD2, segmented_button_selected_color=C_AZUL)
        tabs.pack(fill="both", expand=True, padx=18, pady=10)

        tabs.add(" Biometría y Metas")
        tabs.add(" Plan y Entrenamientos")
        tabs.add(" Récords y Catálogo")

        self._setup_tab_bio(tabs.tab(" Biometría y Metas"), atleta, datos)
        self._setup_tab_plan_entrenos(tabs.tab(" Plan y Entrenamientos"), atleta, datos)
        self._setup_tab_records(tabs.tab(" Récords y Catálogo"), atleta, datos)

    # ═══════════════════════════════════════════════════════
    # TAB 1: BIOMETRÍA Y METAS
    # ═══════════════════════════════════════════════════════
    def _setup_tab_bio(self, tab, atleta, datos):
        tab.configure(fg_color="transparent")
        scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        top_row = ctk.CTkFrame(scroll, fg_color="transparent")
        top_row.pack(fill="x", pady=(8, 0), padx=4)

        f_form = self._card(top_row)
        f_form.pack(side="left", fill="y", padx=(0, 10), pady=4)
        self._label_titulo(f_form, "Registrar Medición").pack(anchor="w", padx=16, pady=(14, 6))
        self._label_muted(f_form, "Actualiza tus datos corporales").pack(anchor="w", padx=16)

        e_grasa = ctk.CTkEntry(f_form, placeholder_text="% Grasa corporal", width=200)
        e_grasa.pack(padx=16, pady=6)
        e_peso = ctk.CTkEntry(f_form, placeholder_text=f"Peso actual (kg) [{atleta.peso}]", width=200)
        e_peso.pack(padx=16, pady=6)

        lbl_ok = ctk.CTkLabel(f_form, text="", font=("Arial", 12), text_color=C_VERDE)
        lbl_ok.pack(padx=16)

        def guardar_medicion():
            try:
                grasa_s = e_grasa.get().strip().replace(',', '.')
                if not grasa_s:
                    lbl_ok.configure(text=" Datos incompletos", text_color=C_AMARILLO)
                    return
                grasa = float(grasa_s)
                p_s = e_peso.get().strip().replace(',', '.')
                peso = float(p_s) if p_s else atleta.peso

                m = MediaCorporal(date.today().strftime("%Y-%m-%d"), grasa, peso)
                self.atletismo.añadir_medida(m)
                datos["biometria"].append((date.today().strftime("%Y-%m-%d"), grasa, peso))
                atleta.peso = peso
                lbl_ok.configure(text="✓ Guardado correctamente", text_color=C_VERDE)
                e_grasa.delete(0, "end")
                e_peso.delete(0, "end")
                _dibujar_graficas()
            except (ValueError, EntidadException) as e:
                lbl_ok.configure(text=" Datos incompletos o erróneos", text_color=C_AMARILLO)

        self._btn(f_form, "Guardar Medición", guardar_medicion, width=200).pack(padx=16, pady=(6,16))

        f_metas = self._card(top_row)
        f_metas.pack(side="left", fill="both", expand=True, pady=4)
        self._label_titulo(f_metas, "Objetivos Activos").pack(anchor="w", padx=16, pady=(14, 6))

        f_lista_metas = ctk.CTkScrollableFrame(f_metas, fg_color="transparent", height=150)
        f_lista_metas.pack(fill="x", padx=12, pady=4)

        def _refrescar_metas():
            for w in f_lista_metas.winfo_children(): w.destroy()
            for tipo, valor, fecha_l in datos["objetivos"]:
                dias_rest = (fecha_l - date.today()).days
                color_dias = C_VERDE if dias_rest > 30 else (C_AMARILLO if dias_rest > 7 else C_ROJO)
                fila = ctk.CTkFrame(f_lista_metas, fg_color=C_CARD2, corner_radius=8, height=42)
                fila.pack(fill="x", pady=3)
                fila.pack_propagate(False)
                ctk.CTkLabel(fila, text=f" {tipo} → {valor}", font=("Arial", 13), text_color=C_TEXTO).pack(side="left", padx=12)
                ctk.CTkLabel(fila, text=f"{dias_rest}d restantes", font=("Arial", 12, "bold"), text_color=color_dias).pack(side="right", padx=12)
        _refrescar_metas()

        f_nueva_meta = ctk.CTkFrame(f_metas, fg_color="transparent")
        f_nueva_meta.pack(fill="x", padx=12, pady=6)
        e_tipo = ctk.CTkEntry(f_nueva_meta, placeholder_text="Tipo de meta", width=180)
        e_tipo.pack(side="left", padx=(0,6))
        e_valor = ctk.CTkEntry(f_nueva_meta, placeholder_text="Valor", width=130)
        e_valor.pack(side="left", padx=(0,6))
        e_dias = ctk.CTkEntry(f_nueva_meta, placeholder_text="Días plazo", width=90)
        e_dias.pack(side="left", padx=(0,6))

        def añadir_meta():
            try:
                tipo = e_tipo.get().strip()
                v_s = e_valor.get().strip().replace(',', '.')
                d_s = e_dias.get().strip()
                if not tipo or not v_s or not d_s:
                    messagebox.showwarning("Aviso", "Datos incompletos")
                    return
                valor = float(v_s)
                dias = int(d_s)
                fec_l = date.today() + timedelta(days=dias)
                o = Objetivo(tipo, valor, fec_l)
                self.atletismo.fijar_objetivo(o)
                datos["objetivos"].append((tipo, valor, fec_l))
                e_tipo.delete(0,"end"); e_valor.delete(0,"end"); e_dias.delete(0,"end")
                _refrescar_metas()
            except (ValueError, EntidadException) as e:
                messagebox.showerror("Error", str(e))

        self._btn(f_nueva_meta, "+", añadir_meta, width=36, height=34).pack(side="left")

        f_graficas = ctk.CTkFrame(scroll, fg_color="transparent")
        f_graficas.pack(fill="x", pady=10, padx=4)

        def _dibujar_graficas():
            for w in f_graficas.winfo_children(): w.destroy()
            bio = datos["biometria"]
            if not bio:
                ctk.CTkLabel(f_graficas, text="Registra mediciones para ver la evolución.", font=("Arial", 14), text_color=C_MUTED).pack(pady=30)
                return
            if not MATPLOTLIB_OK: return

            fechas = [b[0][-5:] for b in bio]
            grasas = [b[1] for b in bio]
            pesos = [b[2] for b in bio]

            fig = Figure(figsize=(11, 4.2), facecolor=C_CARD)
            ax1 = fig.add_subplot(1, 2, 1)
            ax1.set_facecolor(C_CARD)
            ax1.plot(fechas, grasas, color=C_AZUL, marker="o", linewidth=2.5, markersize=6)
            ax1.fill_between(range(len(fechas)), grasas, alpha=0.15, color=C_AZUL)
            ax1.set_title("% Grasa Corporal", color=C_TEXTO, fontsize=13, pad=8)
            ax1.set_xticks(range(len(fechas)))
            ax1.set_xticklabels(fechas, rotation=30, color=C_MUTED, fontsize=8)
            ax1.tick_params(colors=C_MUTED)
            ax1.spines[:].set_color("#263547")
            for label in ax1.get_yticklabels(): label.set_color(C_MUTED)

            ax2 = fig.add_subplot(1, 2, 2)
            ax2.set_facecolor(C_CARD)
            ax2.plot(fechas, pesos, color=C_VERDE, marker="s", linewidth=2.5, markersize=6)
            ax2.fill_between(range(len(fechas)), pesos, alpha=0.15, color=C_VERDE)
            ax2.set_title("Evolución del Peso (kg)", color=C_TEXTO, fontsize=13, pad=8)
            ax2.set_xticks(range(len(fechas)))
            ax2.set_xticklabels(fechas, rotation=30, color=C_MUTED, fontsize=8)
            ax2.tick_params(colors=C_MUTED)
            ax2.spines[:].set_color("#263547")
            for label in ax2.get_yticklabels(): label.set_color(C_MUTED)

            fig.tight_layout(pad=2.0)
            canvas_widget = FigureCanvasTkAgg(fig, master=f_graficas)
            canvas_widget.draw()
            canvas_widget.get_tk_widget().pack(fill="x", pady=6)

        _dibujar_graficas()

    # ═══════════════════════════════════════════════════════
    # TAB 2: PLAN Y ENTRENAMIENTOS
    # ═══════════════════════════════════════════════════════
    def _setup_tab_plan_entrenos(self, tab, atleta, datos):
        tab.configure(fg_color="transparent")

        self._dia_sel = ctk.StringVar(value=self.dia_simulado_var.get())

        ctk.CTkLabel(tab, text="Haz clic en un día del calendario para organizar su rutina y registrar ejercicios.",
                     font=("Arial", 14), text_color=C_MUTED).pack(pady=(10, 0))

        f_dias = ctk.CTkFrame(tab, fg_color="transparent")
        f_dias.pack(fill="x", padx=10, pady=10)

        seg_dias = ctk.CTkSegmentedButton(f_dias, values=self.dias_semana, variable=self._dia_sel,
                                          command=lambda v: _renderizar_panel_dia(v))
        seg_dias.pack(fill="x")

        f_dinamico = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        f_dinamico.pack(fill="both", expand=True)

        def _renderizar_panel_dia(dia):
            for w in f_dinamico.winfo_children(): w.destroy()

            f_forms = ctk.CTkFrame(f_dinamico, fg_color="transparent")
            f_forms.pack(fill="x", pady=10)

            # Rutina del día
            f_plan = self._card(f_forms)
            f_plan.pack(side="left", fill="y", padx=5, expand=True)
            self._label_titulo(f_plan, f"📅 Rutina para el {dia}").pack(pady=(14,5), padx=16, anchor="w")

            tb_plan = ctk.CTkTextbox(f_plan, height=120, fg_color=C_FONDO)
            tb_plan.pack(padx=16, pady=5, fill="x")
            tb_plan.insert("end", datos["plan"].get(dia, "Descanso"))

            lbl_plan_ok = ctk.CTkLabel(f_plan, text="", text_color=C_VERDE)
            lbl_plan_ok.pack()

            def guardar_rutina():
                txt = tb_plan.get("0.0", "end").strip()
                if not txt:
                    lbl_plan_ok.configure(text="Datos incompletos", text_color=C_AMARILLO)
                    return
                datos["plan"][dia] = txt

                dias_activos = [d for d in self.dias_semana if datos["plan"].get(d, "Descanso").lower() != "descanso"]
                rutinas = [datos["plan"].get(d).strip() for d in dias_activos]
                if dias_activos:
                    try:
                        self.gym.programar_semana(dias_activos, rutinas)
                    except Exception: pass
                lbl_plan_ok.configure(text="✓ Rutina guardada", text_color=C_VERDE)

            self._btn(f_plan, "Guardar Rutina", guardar_rutina, color=C_VERDE).pack(pady=10)

            # Registrar entreno
            f_entrenos = self._card(f_forms)
            f_entrenos.pack(side="left", fill="both", padx=5, expand=True)
            self._label_titulo(f_entrenos, f"🏋️ Registrar ejercicio hecho el {dia}").pack(pady=(14,5), padx=16, anchor="w")

            tabs_ent = ctk.CTkTabview(f_entrenos, height=180, segmented_button_selected_color=C_AZUL)
            tabs_ent.pack(fill="both", padx=16, pady=5)
            t_fuerza = tabs_ent.add("Fuerza")
            t_cardio = tabs_ent.add("Cardio")

            # Fuerza
            e_ej_f = ctk.CTkEntry(t_fuerza, placeholder_text="Ejercicio (ej: Sentadilla)", width=270)
            e_ej_f.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

            e_p = ctk.CTkEntry(t_fuerza, placeholder_text="Peso kg", width=130)
            e_p.grid(row=1, column=0, padx=5, pady=5)
            e_r = ctk.CTkEntry(t_fuerza, placeholder_text="Reps", width=130)
            e_r.grid(row=1, column=1, padx=5, pady=5)
            e_d = ctk.CTkEntry(t_fuerza, placeholder_text="Duración min", width=130)
            e_d.grid(row=2, column=0, padx=5, pady=5)

            lbl_f_ok = ctk.CTkLabel(t_fuerza, text="")
            lbl_f_ok.grid(row=2, column=1)

            def log_fuerza():
                ej_txt = e_ej_f.get().strip()
                p_txt = e_p.get().strip().replace(',', '.')
                r_txt = e_r.get().strip()
                d_txt = e_d.get().strip()

                if not ej_txt or not p_txt or not r_txt or not d_txt:
                    lbl_f_ok.configure(text="Datos incompletos", text_color=C_AMARILLO)
                    return
                try:
                    p = float(p_txt); r = int(r_txt); d = int(d_txt)
                    fecha = date.today().strftime("%Y-%m-%d")
                    id_e = len(self.gym._historial_sesiones) + 100
                    ent = EntrenamientoFuerza(fecha, d, p, r, id_e)
                    self.gym.registrar_entrenamiento(ent)
                    datos["sesiones_fuerza"].append((fecha, d, p, r, ej_txt))
                    lbl_f_ok.configure(text="✓ Registrado", text_color=C_VERDE)
                    for e in [e_ej_f, e_p, e_r, e_d]: e.delete(0, "end")
                    _dibujar_graficas_entreno()
                except Exception:
                    lbl_f_ok.configure(text="Datos inválidos", text_color=C_AMARILLO)

            self._btn(t_fuerza, "Añadir Ejercicio", log_fuerza, height=28).grid(row=3, column=0, columnspan=2, pady=10)

            # Cardio
            e_cdist = ctk.CTkEntry(t_cardio, placeholder_text="Distancia km", width=130)
            e_cdist.grid(row=0, column=0, padx=5, pady=5)
            e_cdur = ctk.CTkEntry(t_cardio, placeholder_text="Duración min", width=130)
            e_cdur.grid(row=0, column=1, padx=5, pady=5)
            e_cmin = ctk.CTkEntry(t_cardio, placeholder_text="Ritmo min", width=130)
            e_cmin.grid(row=1, column=0, padx=5, pady=5)
            e_cseg = ctk.CTkEntry(t_cardio, placeholder_text="Ritmo seg", width=130)
            e_cseg.grid(row=1, column=1, padx=5, pady=5)

            lbl_c_ok = ctk.CTkLabel(t_cardio, text="")
            lbl_c_ok.grid(row=2, column=1)

            def log_cardio():
                dist_txt = e_cdist.get().strip().replace(',', '.')
                dur_txt = e_cdur.get().strip()
                min_txt = e_cmin.get().strip()
                seg_txt = e_cseg.get().strip()

                if not dist_txt or not dur_txt or not min_txt or not seg_txt:
                    lbl_c_ok.configure(text="Datos incompletos", text_color=C_AMARILLO)
                    return
                try:
                    dist = float(dist_txt); dur = int(dur_txt)
                    m = int(min_txt); s = int(seg_txt)
                    ritmo = self.gym.definir_ritmo_cardio(m, s)
                    fecha = date.today().strftime("%Y-%m-%d")
                    id_e = len(self.gym._historial_sesiones) + 100
                    entreno = EntrenamientoCardio(fecha, dur, dist, ritmo, id_e)
                    self.gym.registrar_entrenamiento(entreno)
                    datos["sesiones_cardio"].append((fecha, dur, dist, m, s))
                    lbl_c_ok.configure(text="✓ Registrado", text_color=C_VERDE)
                    for e in [e_cdist, e_cdur, e_cmin, e_cseg]: e.delete(0, "end")
                    _dibujar_graficas_entreno()
                except Exception:
                    lbl_c_ok.configure(text="Datos inválidos", text_color=C_AMARILLO)

            self._btn(t_cardio, "Añadir Cardio", log_cardio, height=28).grid(row=2, column=0, pady=10)

            # Gráficas
            f_graficas_e = ctk.CTkFrame(f_dinamico, fg_color="transparent")
            f_graficas_e.pack(fill="x", padx=4, pady=10)

            def _dibujar_graficas_entreno():
                for w in f_graficas_e.winfo_children(): w.destroy()
                sesiones_f = datos["sesiones_fuerza"]
                sesiones_c = datos["sesiones_cardio"]

                if not sesiones_f and not sesiones_c:
                    self._label_muted(f_graficas_e, "Añade ejercicios arriba para ver la gráfica de progreso.").pack(pady=20)
                    return
                if not MATPLOTLIB_OK: return

                fig = Figure(figsize=(11, 4.5), facecolor=C_CARD)
                n_plots = (1 if sesiones_f else 0) + (1 if sesiones_c else 0)
                plot_idx = 1

                if sesiones_f:
                    grupos_dict: dict = {}
                    for fecha, dur, peso_l, reps, grupo in sesiones_f:
                        grupos_dict.setdefault(grupo, []).append((fecha, peso_l * reps))

                    ax = fig.add_subplot(1, n_plots, plot_idx)
                    ax.set_facecolor(C_CARD)
                    colores_g = [C_AZUL, C_VERDE, C_AMARILLO, "#E74C3C", "#9B59B6", "#1ABC9C"]
                    for idx_g, (grupo, vals) in enumerate(grupos_dict.items()):
                        fechas_g = [v[0][-5:] for v in vals]
                        volumen_g = [v[1] for v in vals]
                        color_g = colores_g[idx_g % len(colores_g)]
                        ax.plot(range(len(fechas_g)), volumen_g, marker="o", linewidth=2, markersize=5, label=grupo, color=color_g)

                    ax.set_title("Volumen por Ejercicio (kg)", color=C_TEXTO, fontsize=12, pad=8)
                    ax.set_xticks(range(len(fechas_g)))
                    ax.set_xticklabels(fechas_g, rotation=45, color=C_MUTED, fontsize=9)
                    ax.tick_params(colors=C_MUTED)
                    ax.spines[:].set_color("#263547")
                    for lbl in ax.get_yticklabels(): lbl.set_color(C_MUTED)
                    ax.legend(fontsize=8, facecolor=C_CARD2, labelcolor=C_TEXTO, framealpha=0.8)
                    plot_idx += 1

                if sesiones_c:
                    ax2 = fig.add_subplot(1, n_plots, plot_idx)
                    ax2.set_facecolor(C_CARD)
                    fechas_c = [s[0][-5:] for s in sesiones_c]
                    distancias = [s[2] for s in sesiones_c]
                    ritmos_dec = [s[3] + s[4] / 60 for s in sesiones_c]

                    ax2.bar(range(len(fechas_c)), distancias, color=C_AZUL, alpha=0.7, label="Distancia (km)")
                    ax2.set_title("Cardio: Distancia y Ritmo", color=C_TEXTO, fontsize=12, pad=8)
                    ax2.set_xticks(range(len(fechas_c)))
                    ax2.set_xticklabels(fechas_c, rotation=45, color=C_MUTED, fontsize=9)
                    ax2.tick_params(colors=C_MUTED)
                    ax2.spines[:].set_color("#263547")
                    for lbl in ax2.get_yticklabels(): lbl.set_color(C_MUTED)

                    ax2b = ax2.twinx()
                    ax2b.plot(range(len(fechas_c)), ritmos_dec, color=C_AMARILLO, marker="D", linewidth=2, markersize=5, label="Ritmo min/km")
                    ax2b.tick_params(colors=C_MUTED)
                    ax2b.spines[:].set_color("#263547")
                    for lbl in ax2b.get_yticklabels(): lbl.set_color(C_MUTED)

                fig.tight_layout(pad=2.0)
                canvas_widget = FigureCanvasTkAgg(fig, master=f_graficas_e)
                canvas_widget.draw()
                canvas_widget.get_tk_widget().pack(fill="x", pady=6)

            _dibujar_graficas_entreno()

        _renderizar_panel_dia(self._dia_sel.get())

    # ═══════════════════════════════════════════════════════
    # TAB 3: RÉCORDS Y CATÁLOGO
    # ═══════════════════════════════════════════════════════
    def _setup_tab_records(self, tab, atleta, datos):
        tab.configure(fg_color="transparent")
        scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        f_row = ctk.CTkFrame(scroll, fg_color="transparent")
        f_row.pack(fill="x", padx=4, pady=8)

        f_records = self._card(f_row)
        f_records.pack(side="left", fill="both", expand=True, padx=(0,10), pady=4)
        self._label_titulo(f_records, f" Récords de {atleta._nombre}").pack(anchor="w", padx=16, pady=(14,8))

        f_lista_rec = ctk.CTkScrollableFrame(f_records, fg_color="transparent", height=200)
        f_lista_rec.pack(fill="x", padx=12, pady=4)

        def _refrescar_records():
            for w in f_lista_rec.winfo_children(): w.destroy()
            records_sorted = sorted(datos["records"].items(), key=lambda x: x[1], reverse=True)
            for idx, (ejercicio, marca) in enumerate(records_sorted):
                medal = ["🥇", "🥈", "🥉"][idx] if idx < 3 else "  "
                fila = ctk.CTkFrame(f_lista_rec, fg_color=C_CARD2, corner_radius=8, height=44)
                fila.pack(fill="x", pady=3)
                fila.pack_propagate(False)
                ctk.CTkLabel(fila, text=f"{medal} {ejercicio}", font=("Arial", 13), text_color=C_TEXTO).pack(side="left", padx=12)
                ctk.CTkLabel(fila, text=f"{marca} kg", font=("Arial", 13, "bold"), text_color=C_AZUL).pack(side="right", padx=12)

        _refrescar_records()

        self._label_muted(f_records, "Actualizar / Añadir récord:").pack(anchor="w", padx=16, pady=(8,2))
        f_frec = ctk.CTkFrame(f_records, fg_color="transparent")
        f_frec.pack(fill="x", padx=12, pady=4)
        e_ej = ctk.CTkEntry(f_frec, placeholder_text="Ejercicio", width=160)
        e_ej.pack(side="left", padx=(0,6))
        e_marca = ctk.CTkEntry(f_frec, placeholder_text="Marca (kg)", width=110)
        e_marca.pack(side="left", padx=(0,6))

        lbl_rec_ok = ctk.CTkLabel(f_records, text="", font=("Arial", 12))
        lbl_rec_ok.pack(padx=16)

        def guardar_record():
            try:
                ej_nombre = e_ej.get().strip()
                m_str = e_marca.get().strip().replace(',', '.')
                if not ej_nombre or not m_str:
                    lbl_rec_ok.configure(text="Datos incompletos", text_color=C_AMARILLO)
                    return
                marca = float(m_str)
                ej_obj = Ejercicio(ej_nombre, "General", "")
                self.atletismo.actualizar_record(ej_obj, marca)
                datos["records"][ej_nombre] = max(datos["records"].get(ej_nombre, 0), marca)
                lbl_rec_ok.configure(text=f"✓ Récord guardado", text_color=C_VERDE)
                e_ej.delete(0,"end"); e_marca.delete(0,"end")
                _refrescar_records(); _dibujar_ranking()
            except (ValueError, EntidadException):
                lbl_rec_ok.configure(text="Datos inválidos", text_color=C_ROJO)

        self._btn(f_frec, "Guardar", guardar_record, width=80, height=34).pack(side="left")

        f_cat = self._card(f_row)
        f_cat.pack(side="left", fill="both", expand=True, pady=4)
        self._label_titulo(f_cat, " Catálogo de Ejercicios").pack(anchor="w", padx=16, pady=(14,8))

        GRUPOS_CAT = ["Pecho", "Espalda", "Piernas", "Hombros", "Bíceps", "Tríceps", "Glúteos", "Core"]
        EJERCICIOS_BASE = {
            "Pecho": ["Press Banca", "Press Inclinado", "Fondos"],
            "Espalda": ["Peso Muerto", "Dominadas", "Remo con Barra"],
            "Piernas": ["Sentadilla", "Prensa", "Zancadas"],
            "Hombros": ["Press Militar", "Elevaciones Lat."],
            "Bíceps": ["Curl Barra", "Curl Alterno"],
            "Tríceps": ["Fondos Tríceps", "Press Francés"],
            "Glúteos": ["Hip Thrust", "Sentadilla Búlgara"],
            "Core": ["Plancha", "Abdominales"],
        }

        f_cat_scroll = ctk.CTkScrollableFrame(f_cat, fg_color="transparent", height=200)
        f_cat_scroll.pack(fill="x", padx=12, pady=4)

        for grupo, ejercs in EJERCICIOS_BASE.items():
            ctk.CTkLabel(f_cat_scroll, text=grupo, font=("Arial", 12, "bold"), text_color=C_AZUL).pack(anchor="w", pady=(6,2))
            fila_ej = ctk.CTkFrame(f_cat_scroll, fg_color="transparent")
            fila_ej.pack(fill="x")
            for ej in ejercs:
                badge = ctk.CTkFrame(fila_ej, fg_color=C_CARD2, corner_radius=6, height=28)
                badge.pack(side="left", padx=3, pady=2)
                badge.pack_propagate(False)
                ctk.CTkLabel(badge, text=ej, font=("Arial", 11), text_color=C_TEXTO).pack(padx=8, expand=True)

        self._label_muted(f_cat, "Añadir ejercicio al catálogo:").pack(anchor="w", padx=16, pady=(8,2))
        f_fej = ctk.CTkFrame(f_cat, fg_color="transparent")
        f_fej.pack(fill="x", padx=12, pady=4)
        e_nuevo_ej = ctk.CTkEntry(f_fej, placeholder_text="Nombre ejercicio", width=160)
        e_nuevo_ej.pack(side="left", padx=(0,6))
        opt_grp_cat = ctk.CTkOptionMenu(f_fej, values=GRUPOS_CAT, width=120)
        opt_grp_cat.pack(side="left", padx=(0,6))

        def añadir_ejercicio():
            nom = e_nuevo_ej.get().strip()
            if not nom:
                messagebox.showwarning("Aviso", "Datos incompletos")
                return
            try:
                grp = opt_grp_cat.get()
                self.gym.crear_ejercicio(nom, grp, "Ejercicio personalizado")
                e_nuevo_ej.delete(0,"end")
                messagebox.showinfo("Catálogo", f"Ejercicio '{nom}' añadido.")
            except ServicioException as e: messagebox.showerror("Error", str(e))

        self._btn(f_fej, "Añadir", añadir_ejercicio, width=80, height=34).pack(side="left")

        # ── Ranking ────
        f_ranking = self._card(scroll)
        f_ranking.pack(fill="x", padx=4, pady=8)
        self._label_titulo(f_ranking, " Ranking de Récords (Todos los Atletas)").pack(anchor="w", padx=16, pady=(14,8))

        f_ranking_contenido = ctk.CTkFrame(f_ranking, fg_color="transparent")
        f_ranking_contenido.pack(fill="x", padx=12, pady=(0,14))

        def _dibujar_ranking():
            for w in f_ranking_contenido.winfo_children(): w.destroy()
            todos_ejercicios: dict[str, list[tuple]] = {}
            for a in self.atletismo.obtener_todos():
                ex = self._get_extra(a._nombre)
                for ej, marca in ex["records"].items():
                    todos_ejercicios.setdefault(ej, []).append((a._nombre, marca))
            if not todos_ejercicios: return

            cols = 3
            for idx, (ejercicio, marcas) in enumerate(todos_ejercicios.items()):
                row_idx = idx // cols
                col_idx = idx % cols
                marcas_sorted = sorted(marcas, key=lambda x: x[1], reverse=True)

                f_ej_card = ctk.CTkFrame(f_ranking_contenido, fg_color=C_CARD2, corner_radius=10)
                f_ej_card.grid(row=row_idx, column=col_idx, padx=8, pady=8, sticky="nsew")
                f_ranking_contenido.grid_columnconfigure(col_idx, weight=1)

                ctk.CTkLabel(f_ej_card, text=ejercicio, font=("Arial", 13, "bold"), text_color=C_AMARILLO).pack(pady=(10,4), padx=10)
                for pos, (nombre, marca) in enumerate(marcas_sorted):
                    medal = ["🥇", "🥈", "🥉"][pos] if pos < 3 else f"{pos+1}."
                    color_nombre = C_AZUL if nombre == atleta._nombre else C_TEXTO
                    fila = ctk.CTkFrame(f_ej_card, fg_color="transparent")
                    fila.pack(fill="x", padx=10, pady=2)
                    ctk.CTkLabel(fila, text=f"{medal} {nombre}", font=("Arial", 12), text_color=color_nombre).pack(side="left")
                    ctk.CTkLabel(fila, text=f"{marca} kg", font=("Arial", 12, "bold"), text_color=C_VERDE).pack(side="right")
                ctk.CTkFrame(f_ej_card, fg_color="transparent", height=8).pack()

        _dibujar_ranking()

    # ─────────────────────────────────────────
    # RANKING GLOBAL
    # ─────────────────────────────────────────
    def mostrar_ranking_global(self):
        self.limpiar_pantalla()
        self.atleta_actual = None
        self._header(self.main_frame, " Ranking Global de Todos los Atletas", boton_volver=self.mostrar_dashboard)

        scroll = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=24, pady=16)

        atletas = self.atletismo.obtener_todos()
        if not atletas: return

        f_tabla = self._card(scroll)
        f_tabla.pack(fill="x", pady=(0,16))
        self._label_titulo(f_tabla, " Métricas Generales").pack(anchor="w", padx=16, pady=(14,8))

        cabeceras = ["Atleta", "IMC", "Sesiones Fuerza", "Sesiones Cardio", "Km Totales", "Récords"]
        f_head = ctk.CTkFrame(f_tabla, fg_color=C_CARD2, height=36, corner_radius=0)
        f_head.pack(fill="x", padx=12)
        f_head.pack_propagate(False)
        for i, c in enumerate(cabeceras):
            ctk.CTkLabel(f_head, text=c, font=("Arial", 12, "bold"), text_color=C_AZUL, width=150 if i==0 else 110).pack(side="left", padx=8)

        for atleta in atletas:
            datos = self._get_extra(atleta._nombre)
            try: imc = self.atletismo.calcular_imc_atleta(atleta)
            except: imc = 0.0
            km_totales = sum(s[2] for s in datos["sesiones_cardio"])
            n_fuerza = len(datos["sesiones_fuerza"])
            n_cardio = len(datos["sesiones_cardio"])
            n_records = len(datos["records"])

            fila = ctk.CTkFrame(f_tabla, fg_color="transparent", height=38)
            fila.pack(fill="x", padx=12, pady=2)
            fila.pack_propagate(False)
            for i, val in enumerate([atleta._nombre, f"{imc}", str(n_fuerza), str(n_cardio), f"{km_totales:.1f} km", str(n_records)]):
                ctk.CTkLabel(fila, text=val, font=("Arial", 12), text_color=C_TEXTO if i>0 else C_AZUL, width=150 if i==0 else 110).pack(side="left", padx=8)

        f_podio = self._card(scroll)
        f_podio.pack(fill="x", pady=8)
        self._label_titulo(f_podio, " Mejores Marcas Absolutas").pack(anchor="w", padx=16, pady=(14,8))

        todos_ej: dict = {}
        for a in atletas:
            for ej, marca in self._get_extra(a._nombre)["records"].items():
                if ej not in todos_ej or marca > todos_ej[ej][1]:
                    todos_ej[ej] = (a._nombre, marca)

        f_pod_row = ctk.CTkFrame(f_podio, fg_color="transparent")
        f_pod_row.pack(fill="x", padx=12, pady=(0,14))
        for idx, (ej, (nombre, marca)) in enumerate(sorted(todos_ej.items(), key=lambda x: x[1][1], reverse=True)):
            medal = ["🥇", "🥈", "🥉"][idx] if idx < 3 else " "
            f_item = ctk.CTkFrame(f_pod_row, fg_color=C_CARD2, corner_radius=8, height=50)
            f_item.pack(side="left", expand=True, fill="x", padx=6)
            f_item.pack_propagate(False)
            ctk.CTkLabel(f_item, text=f"{medal} {ej}", font=("Arial", 12, "bold"), text_color=C_TEXTO).pack(anchor="w", padx=10, pady=(8,0))
            ctk.CTkLabel(f_item, text=f"{nombre} • {marca} kg", font=("Arial", 11), text_color=C_VERDE).pack(anchor="w", padx=10)

        if MATPLOTLIB_OK and len(atletas) > 1:
            f_graf_rank = self._card(scroll)
            f_graf_rank.pack(fill="x", pady=8)
            self._label_titulo(f_graf_rank, " Comparativa de Volumen Total (kg levantados)").pack(anchor="w", padx=16, pady=(14,8))

            nombres_g = []
            volumenes_g = []
            for a in atletas:
                vol = sum(s[2]*s[3] for s in self._get_extra(a._nombre)["sesiones_fuerza"])
                nombres_g.append(a._nombre.split()[0])
                volumenes_g.append(vol)

            fig2 = Figure(figsize=(9, 3.4), facecolor=C_CARD)
            ax = fig2.add_subplot(1,1,1)
            ax.set_facecolor(C_CARD)
            barras = ax.bar(range(len(nombres_g)), volumenes_g, color=[C_AZUL, C_VERDE, C_AMARILLO][:len(nombres_g)], alpha=0.85, width=0.5)
            ax.set_xticks(range(len(nombres_g)))
            ax.set_xticklabels(nombres_g, color=C_TEXTO, fontsize=11)
            ax.tick_params(colors=C_MUTED)
            ax.spines[:].set_color("#263547")
            for lbl in ax.get_yticklabels(): lbl.set_color(C_MUTED)

            fig2.tight_layout(pad=2.0)
            canvas2 = FigureCanvasTkAgg(fig2, master=f_graf_rank)
            canvas2.draw()
            canvas2.get_tk_widget().pack(fill="x", padx=12, pady=(0,14))

    # ─────────────────────────────────────────
    # MODALES AÑADIR / ELIMINAR ATLETA
    # ─────────────────────────────────────────
    def modal_añadir_alumno(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Añadir nuevo atleta")
        dialog.geometry("380x320")
        dialog.attributes("-topmost", True)
        dialog.configure(fg_color=C_FONDO)

        self._label_titulo(dialog, "Nuevo Atleta").pack(pady=(24,6))
        self._label_muted(dialog, "Introduce los datos básicos").pack()

        e_nom = ctk.CTkEntry(dialog, placeholder_text="Nombre completo", width=260)
        e_nom.pack(pady=8)
        e_peso = ctk.CTkEntry(dialog, placeholder_text="Peso (kg)", width=260)
        e_peso.pack(pady=8)
        e_alt = ctk.CTkEntry(dialog, placeholder_text="Altura (m)", width=260)
        e_alt.pack(pady=8)
        lbl_err = ctk.CTkLabel(dialog, text="", font=("Arial", 12), text_color=C_ROJO)
        lbl_err.pack()

        def confirmar():
            nom = e_nom.get().strip()
            p_s = e_peso.get().strip().replace(',', '.')
            a_s = e_alt.get().strip().replace(',', '.')

            if not nom or not p_s or not a_s:
                lbl_err.configure(text="Datos incompletos", text_color=C_AMARILLO)
                return

            try:
                self.atletismo.registrar_atleta(nom, float(p_s), float(a_s))
                self._renderizar_tarjetas()
                dialog.destroy()
            except (ValueError, EntidadException, ServicioException) as e:
                lbl_err.configure(text=str(e))

        self._btn(dialog, "Crear Atleta", confirmar, color=C_VERDE, width=200, height=40).pack(pady=14)

    def modal_eliminar_alumno(self):
        atletas = self.atletismo.obtener_todos()
        if not atletas:
            messagebox.showinfo("Sin atletas", "No hay atletas para eliminar.")
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title("Eliminar atleta")
        dialog.geometry("360x240")
        dialog.attributes("-topmost", True)
        dialog.configure(fg_color=C_FONDO)

        self._label_titulo(dialog, "Eliminar Atleta").pack(pady=(24,6))
        ctk.CTkLabel(dialog, text="Esta acción no se puede deshacer.", font=("Arial", 12), text_color=C_ROJO).pack()

        nombres = [a._nombre for a in atletas]
        cbox = ctk.CTkComboBox(dialog, values=nombres, width=280)
        cbox.pack(pady=16)

        def confirmar():
            nombre = cbox.get()
            if not nombre: return

            # ELIMINACIÓN SEGURA
            for a in list(self.atletismo._atletas):
                if a._nombre == nombre:
                    self.atletismo._atletas.remove(a)
                    self._datos_extra.pop(nombre, None)
                    break
            self._renderizar_tarjetas()
            dialog.destroy()

        self._btn(dialog, "Eliminar Definitivamente", confirmar, color=C_ROJO, width=240, height=40).pack(pady=8)

    # ─────────────────────────────────────────
    # FIX: CIERRE SEGURO DE LA APLICACIÓN
    # ─────────────────────────────────────────
    def cerrar_aplicacion(self):
        try:
            self.atletismo.guardar_estado()
            self.gym.guardar_estado()
            # Guardamos los datos de las nuevas gráficas y récords
            os.makedirs("data", exist_ok=True)
            ManejadorArchivos.guardar_binario("data/extra_data.pkl", self._datos_extra)
        except Exception as e:
            print(f"Error al guardar: {e}")
        finally:
            self.quit()
            self.destroy()
            sys.exit(0)

# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = UAFitnessCoachApp()
    app.mainloop()