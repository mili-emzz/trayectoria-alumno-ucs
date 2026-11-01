"""
main.py — Punto de entrada del Planificador de Trayectoria Académica
Ejecutar con:  python main.py
"""

import tkinter as tk
from src.ui import AcademicPlannerApp


if __name__ == "__main__":
    root = tk.Tk()
    app = AcademicPlannerApp(root)
    root.mainloop()
