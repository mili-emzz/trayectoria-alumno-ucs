"""
ui.py — Interfaz gráfica Tkinter
Planificador de Trayectoria Académica — Ingeniería en Software
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading

from src.curriculum import MATERIAS, TODAS_LAS_MATERIAS
from src.solver import ucs


# ── Clase utilitaria para Tooltips ──────────────────────────────────────────

def validar_aprobadas(aprobadas: set, cuatrimestre: int) -> list:
    """
    Valida las materias marcadas como aprobadas contra el cuatrimestre actual.

    Un alumno que está por cursar el cuatrimestre N solo pudo haber aprobado
    materias de los cuatrimestres 1 a N-1: una materia de nivel N o superior
    todavía no ha podido cursarse.

    Devuelve una lista de mensajes de error (vacía si todo es válido).
    """
    errores = []

    futuras = sorted(
        (m for m in aprobadas if MATERIAS[m]["cuatrimestre"] >= cuatrimestre),
        key=lambda m: (MATERIAS[m]["cuatrimestre"], MATERIAS[m]["nombre"]),
    )
    if futuras:
        detalle = "\n".join(
            f"   • {MATERIAS[m]['nombre']} (cuatrimestre {MATERIAS[m]['cuatrimestre']})"
            for m in futuras
        )
        if cuatrimestre == 1:
            regla = "En el cuatrimestre 1 el alumno aún no puede tener materias aprobadas."
        else:
            regla = (f"Un alumno en el cuatrimestre {cuatrimestre} solo puede tener "
                     f"aprobadas materias de los cuatrimestres 1 a {cuatrimestre - 1}.")
        errores.append(
            "Marcaste como aprobadas materias que todavía no corresponden:\n"
            f"{detalle}\n\n{regla}\n"
            "Desmárcalas o cambia el cuatrimestre actual."
        )

    return errores


class Tooltip:
    """Muestra una ventana emergente con texto de ayuda al pasar el mouse."""

    def __init__(self, widget: tk.Widget, text: str):
        self.widget = widget
        self.text = text
        self._tip_window: tk.Toplevel | None = None
        widget.bind("<Enter>", self._show)
        widget.bind("<Leave>", self._hide)

    def _show(self, _event=None):
        if self._tip_window:
            return
        x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
        self._tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)   # Sin bordes de ventana
        tw.wm_geometry(f"+{x}+{y}")
        tk.Label(
            tw, text=self.text,
            bg="#45475a", fg="#cdd6f4",
            font=("Segoe UI", 9),
            relief="flat", padx=8, pady=5,
            wraplength=280, justify="left",
        ).pack()

    def _hide(self, _event=None):
        if self._tip_window:
            self._tip_window.destroy()
            self._tip_window = None

# ── Paleta de colores (Catppuccin Mocha) ────────────────────────────────────
BG       = "#1e1e2e"
FG       = "#cdd6f4"
ACCENT   = "#89b4fa"
SUCCESS  = "#a6e3a1"
WARNING  = "#f9e2af"
ERROR    = "#f38ba8"
PANEL    = "#313244"
SUBPANEL = "#45475a"


class AcademicPlannerApp:
    """Ventana principal del planificador de trayectoria académica."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Planificador de Trayectoria Académica — IS")
        self.root.configure(bg=BG)
        self.root.geometry("1200x750")
        self.root.minsize(900, 600)

        # Variables de estado del formulario
        self.var_cuatri = tk.IntVar(value=4)
        self.vars_aprobadas = {mid: tk.BooleanVar(value=False) for mid in MATERIAS}

        self._build_ui()

    # ── Construcción de la interfaz ──────────────────────────────────────────

    def _build_ui(self):
        """Construye todos los widgets de la ventana."""

        # Título
        tk.Label(
            self.root,
            text="🎓 Planificador de Trayectoria Académica — Ingeniería en Software",
            bg=BG, fg=ACCENT,
            font=("Segoe UI", 14, "bold"),
            pady=10,
        ).pack(fill="x")

        # Marco principal (divide izquierda / derecha)
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True, padx=10, pady=5)

        self._build_left_panel(main)
        self._build_right_panel(main)

        # Barra de estado
        self.status_var = tk.StringVar(value="Listo. Configura el alumno y presiona Resolver.")
        tk.Label(
            self.root,
            textvariable=self.status_var,
            bg=SUBPANEL, fg=FG,
            font=("Segoe UI", 9),
            anchor="w", padx=10, pady=4,
        ).pack(fill="x", side="bottom")

    def _build_left_panel(self, parent: tk.Frame):
        """Panel izquierdo: configuración del alumno y lista de materias."""

        left = tk.Frame(parent, bg=PANEL, bd=0, relief="flat", width=390)
        left.pack(side="left", fill="y", padx=(0, 8))
        left.pack_propagate(False)

        tk.Label(
            left,
            text="⚙ Configuración del Alumno",
            bg=PANEL, fg=ACCENT,
            font=("Segoe UI", 11, "bold"),
            pady=8,
        ).pack(fill="x", padx=10)

        # Selector de cuatrimestre
        cuatri_frame = tk.Frame(left, bg=PANEL)
        cuatri_frame.pack(fill="x", padx=10, pady=5)
        lbl_cuatri = tk.Label(
            cuatri_frame,
            text="Cuatrimestre actual:",
            bg=PANEL, fg=FG,
            font=("Segoe UI", 10),
        )
        lbl_cuatri.pack(side="left")
        Tooltip(lbl_cuatri,
                "El cuatrimestre en el que estás actualmente.\n"
                "Usa las flechas ▲▼ o escribe el número directamente.\n\n"
                "Ejemplo: si acabas de terminar el 3er cuatrimestre\n"
                "y vas a empezar el 4to, pon 4.")
        spn = tk.Spinbox(
            cuatri_frame,
            from_=1, to=10,
            textvariable=self.var_cuatri,
            width=5,
            font=("Segoe UI", 10),
            bg=SUBPANEL, fg=FG,
            buttonbackground=SUBPANEL,
            relief="flat",
        )
        spn.pack(side="left", padx=8)
        Tooltip(spn,
                "El cuatrimestre en el que estás actualmente (1–10).\n"
                "Úsalo con 👤 Regular para marcar automáticamente\n"
                "las materias de cuatrimestres anteriores.")

        # Botones de acción
        btn_frame = tk.Frame(left, bg=PANEL)
        btn_frame.pack(fill="x", padx=10, pady=5)

        btn_resolver = tk.Button(
            btn_frame,
            text="✅ Resolver",
            command=self._run_solver,
            bg=ACCENT, fg="#1e1e2e",
            font=("Segoe UI", 10, "bold"),
            relief="flat", padx=12, pady=6,
            cursor="hand2",
        )
        btn_resolver.pack(side="left", padx=4)
        Tooltip(btn_resolver,
                "Ejecuta el algoritmo UCS y calcula el plan de materias\n"
                "más corto para graduarte desde tu situación actual.\n\n"
                "Asegúrate de configurar el cuatrimestre y marcar\n"
                "las materias que ya aprobaste antes de presionar.")

        btn_limpiar = tk.Button(
            btn_frame,
            text="🔄 Limpiar",
            command=self._clear,
            bg=SUBPANEL, fg=FG,
            font=("Segoe UI", 10),
            relief="flat", padx=10, pady=6,
            cursor="hand2",
        )
        btn_limpiar.pack(side="left", padx=4)
        Tooltip(btn_limpiar,
                "Desmarca TODAS las materias y borra el resultado.\n"
                "Úsalo para empezar la configuración desde cero.")

        btn_regular = tk.Button(
            btn_frame,
            text="👤 Regular",
            command=self._set_regular,
            bg=SUBPANEL, fg=FG,
            font=("Segoe UI", 10),
            relief="flat", padx=10, pady=6,
            cursor="hand2",
        )
        btn_regular.pack(side="left", padx=4)
        Tooltip(btn_regular,
                "Marca automáticamente como aprobadas todas las materias\n"
                "de los cuatrimestres ANTERIORES al que configuraste.\n\n"
                "Ejemplo: si tienes cuatrimestre 4, marcará todo\n"
                "lo de los cuatrimestres 1, 2 y 3.\n\n"
                "Después puedes desmarcar manualmente cualquier\n"
                "materia que hayas reprobado.")

        # Sección de ayuda rápida
        help_frame = tk.Frame(left, bg=SUBPANEL, bd=0)
        help_frame.pack(fill="x", padx=10, pady=(0, 6))
        tk.Label(
            help_frame,
            text=(
                "💡 Cómo usar:\n"
                "  1. Pon tu cuatrimestre actual en el selector ▲▼\n"
                "  2. Marca las materias que ya aprobaste  ☑\n"
                "     (o usa 👤 Regular si no reprobaste nada)\n"
                "  3. Presiona ✅ Resolver"
            ),
            bg=SUBPANEL, fg="#b4befe",
            font=("Segoe UI", 8),
            justify="left",
            padx=8, pady=6,
            anchor="w",
        ).pack(fill="x")

        # Lista de materias con scroll
        tk.Label(
            left,
            text="📋 Materias aprobadas (marca las que ya cursaste):",
            bg=PANEL, fg=FG,
            font=("Segoe UI", 9),
            pady=4,
        ).pack(fill="x", padx=10)

        canvas = tk.Canvas(left, bg=PANEL, highlightthickness=0)
        scrollbar = ttk.Scrollbar(left, orient="vertical", command=canvas.yview)
        self.subjects_frame = tk.Frame(canvas, bg=PANEL)

        self.subjects_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )

        canvas.create_window((0, 0), window=self.subjects_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)

        # Scroll con rueda del mouse
        canvas.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"),
        )

        # Agrupar materias por cuatrimestre
        grupos: dict = {}
        for mid, data in MATERIAS.items():
            grupos.setdefault(data["cuatrimestre"], []).append((mid, data))

        for q in sorted(grupos.keys()):
            tk.Label(
                self.subjects_frame,
                text=f"── Cuatrimestre {q} ──",
                bg=PANEL, fg=WARNING,
                font=("Segoe UI", 8, "bold"),
            ).pack(anchor="w", padx=8, pady=(6, 0))

            for mid, data in sorted(grupos[q], key=lambda x: x[1]["nombre"]):
                tk.Checkbutton(
                    self.subjects_frame,
                    text=f"  {data['nombre']}",
                    variable=self.vars_aprobadas[mid],
                    bg=PANEL, fg=FG,
                    selectcolor=SUBPANEL,
                    activebackground=PANEL,
                    activeforeground=FG,
                    font=("Segoe UI", 9),
                    anchor="w",
                ).pack(fill="x", padx=12, pady=1)

    def _build_right_panel(self, parent: tk.Frame):
        """Panel derecho: visualización del plan resultante."""

        right = tk.Frame(parent, bg=PANEL)
        right.pack(side="left", fill="both", expand=True)

        tk.Label(
            right,
            text="📊 Plan de Trayectoria Óptimo",
            bg=PANEL, fg=ACCENT,
            font=("Segoe UI", 11, "bold"),
            pady=8,
        ).pack(fill="x", padx=10)

        # Leyenda de colores
        legend_frame = tk.Frame(right, bg=SUBPANEL)
        legend_frame.pack(fill="x", padx=10, pady=(0, 4))
        tk.Label(
            legend_frame,
            text="Cómo leer el resultado:",
            bg=SUBPANEL, fg="#b4befe",
            font=("Segoe UI", 8, "bold"),
            padx=6, pady=3,
        ).pack(anchor="w")
        leyendas = [
            (ACCENT,   "Encabezado / estadísticas generales del plan"),
            (WARNING,  "[CUATRIMESTRE N] — cada bloque es un periodo"),
            (FG,       "• Materia — las que debes tomar ese cuatrimestre"),
            (SUCCESS,  "🎉 Meta — ¡llegaste a Estancia II!"),
            ("#b4befe", "Estadísticas UCS (nodos, tiempo de cómputo)"),
        ]
        for color, desc in leyendas:
            row = tk.Frame(legend_frame, bg=SUBPANEL)
            row.pack(anchor="w", padx=6, pady=1)
            tk.Label(row, text="█", bg=SUBPANEL, fg=color,
                     font=("Segoe UI", 9)).pack(side="left")
            tk.Label(row, text=f" {desc}", bg=SUBPANEL, fg="#cdd6f4",
                     font=("Segoe UI", 8)).pack(side="left")

        self.result_text = scrolledtext.ScrolledText(
            right,
            bg="#11111b", fg=FG,
            font=("Consolas", 10),
            relief="flat", padx=12, pady=8,
            wrap="word",
            insertbackground=FG,
        )
        self.result_text.pack(fill="both", expand=True, padx=10, pady=(0, 5))

        # Mensaje de bienvenida en el área de resultados
        self.result_text.insert(
            tk.END,
            "Aquí aparecerá tu plan de trayectoria académica.\n\n"
            "  1️⃣  Configura tu cuatrimestre actual (panel izquierdo)\n"
            "  2️⃣  Marca las materias que ya aprobaste  ☑\n"
            "         (o usa 👤 Regular si eres alumno sin irregularidades)\n"
            "  3️⃣  Presiona  ✅ Resolver\n\n"
            "💡 Pasa el mouse sobre los botones para ver para qué sirven.\n",
        )
        self.result_text.config(state="disabled")  # solo lectura hasta que haya resultado

        # Etiquetas de color para el texto de resultados
        self.result_text.tag_config("header",  foreground=ACCENT,   font=("Consolas", 11, "bold"))
        self.result_text.tag_config("quarter", foreground=WARNING,   font=("Consolas", 10, "bold"))
        self.result_text.tag_config("subject", foreground=FG)
        self.result_text.tag_config("goal",    foreground=SUCCESS,   font=("Consolas", 11, "bold"))
        self.result_text.tag_config("stats",   foreground="#b4befe")
        self.result_text.tag_config("error",   foreground=ERROR)

    # ── Lógica de los botones ────────────────────────────────────────────────

    def _clear(self):
        """Desmarca todas las materias y limpia el panel de resultados."""
        for v in self.vars_aprobadas.values():
            v.set(False)
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(
            tk.END,
            "Panel limpiado. Configura el alumno y presiona ✅ Resolver.\n",
        )
        self.result_text.config(state="disabled")
        self.status_var.set("Limpiado. Configura el alumno y presiona Resolver.")

    def _set_regular(self):
        """Marca como aprobadas todas las materias de cuatrimestres anteriores al actual."""
        cuatri = self.var_cuatri.get()
        for mid, data in MATERIAS.items():
            self.vars_aprobadas[mid].set(data["cuatrimestre"] < cuatri)
        self.status_var.set(
            f"Alumno regular: materias de cuatrimestres 1–{cuatri - 1} marcadas como aprobadas."
        )

    def _run_solver(self):
        """Lanza el UCS en un hilo secundario para no bloquear la UI."""
        aprobadas = {mid for mid, v in self.vars_aprobadas.items() if v.get()}
        cuatri = self.var_cuatri.get()

        # Validar los datos de entrada antes de lanzar la búsqueda
        errores = validar_aprobadas(aprobadas, cuatri)
        if errores:
            self.status_var.set("Datos inválidos: corrige las materias aprobadas.")
            messagebox.showerror("Materias aprobadas inválidas", "\n\n".join(errores))
            return

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, "⏳ Ejecutando UCS…\n\n", "header")
        self.status_var.set("Ejecutando búsqueda UCS…")
        self.root.update()

        def _worker():
            resultado = ucs(aprobadas, cuatri, callback=self._update_status)
            # Actualizar la UI desde el hilo principal
            self.root.after(0, lambda: self._show_result(resultado, cuatri))

        threading.Thread(target=_worker, daemon=True).start()

    def _update_status(self, msg: str):
        """Callback seguro para actualizar la barra de estado desde otro hilo."""
        self.status_var.set(msg)

    # ── Presentación de resultados ───────────────────────────────────────────

    def _show_result(self, resultado, cuatri_inicial: int):
        """Renderiza el plan óptimo (o el mensaje de error) en el panel derecho."""
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)

        if resultado is None:
            self.result_text.insert(tk.END, "❌ No se encontró solución.\n", "error")
            self.result_text.insert(
                tk.END,
                "Verifica que las materias aprobadas sean consistentes con la seriación.\n",
                "error",
            )
            self.status_var.set("Sin solución.")
            self.result_text.config(state="disabled")
            return

        sep = "═" * 62 + "\n"

        # Encabezado
        self.result_text.insert(tk.END, sep, "header")
        self.result_text.insert(tk.END, "   PLAN DE TRAYECTORIA ÓPTIMO — INTELIGENCIA ARTIFICIAL\n", "header")
        self.result_text.insert(tk.END, sep, "header")
        self.result_text.insert(tk.END, f"  Cuatrimestre de inicio   : {cuatri_inicial}\n", "stats")
        self.result_text.insert(tk.END, f"  Costo total acumulado    : {resultado['costo_total']}\n", "stats")
        self.result_text.insert(tk.END, f"  Periodos hasta graduación: {resultado['cuatrimestres']}\n\n", "stats")

        # Plan cuatrimestre a cuatrimestre
        for paso in resultado["plan"]:
            carga = len(paso["materias"])
            self.result_text.insert(
                tk.END,
                f"[CUATRIMESTRE {paso['cuatrimestre']}]  "
                f"(Carga: {carga} materia{'s' if carga != 1 else ''})\n",
                "quarter",
            )
            for nombre in paso["nombres"]:
                self.result_text.insert(tk.END, f"   • {nombre}\n", "subject")
            self.result_text.insert(tk.END, "\n")

        # Meta alcanzada
        self.result_text.insert(tk.END, "🎉 ¡ESTADO META ALCANZADO — GRADUACIÓN! 🎉\n\n", "goal")

        # Estadísticas del algoritmo
        self.result_text.insert(tk.END, sep, "stats")
        self.result_text.insert(tk.END, "  ESTADÍSTICAS DEL ALGORITMO UCS\n", "stats")
        self.result_text.insert(tk.END, sep, "stats")
        self.result_text.insert(tk.END, f"  Nodos expandidos  : {resultado['nodos_expandidos']}\n", "stats")
        self.result_text.insert(tk.END, f"  Nodos generados   : {resultado['nodos_generados']}\n", "stats")
        self.result_text.insert(tk.END, f"  Tiempo de cómputo : {resultado['tiempo_seg']} segundos\n", "stats")
        self.result_text.insert(tk.END, sep, "stats")

        self.status_var.set(
            f"✅ Solución encontrada en {resultado['tiempo_seg']}s | "
            f"{resultado['cuatrimestres']} periodos | "
            f"{resultado['nodos_expandidos']} nodos expandidos"
        )
        self.result_text.config(state="disabled")