"""
curriculum.py — Catálogo de materias y grafo de prerequisitos
Ingeniería en Software (IS) — Planificador de Trayectoria Académica
"""

# ---------------------------------------------------------------------------
# Catálogo completo de materias
# Cada entrada tiene:
#   nombre      : nombre legible de la materia
#   cuatrimestre: nivel en el plan (1-10)
#   prereqs     : lista de IDs que deben estar aprobados antes
# ---------------------------------------------------------------------------
MATERIAS = {
    # ── CUATRIMESTRE 1 (sin prerequisitos) ─────────────────────────────────
    "ALG":  {"nombre": "Algoritmos",                                   "cuatrimestre": 1, "prereqs": []},
    "FC":   {"nombre": "Fundamentos de Computación",                   "cuatrimestre": 1, "prereqs": []},
    "AL":   {"nombre": "Álgebra Lineal",                               "cuatrimestre": 1, "prereqs": []},
    "CD":   {"nombre": "Cálculo Diferencial",                          "cuatrimestre": 1, "prereqs": []},
    "MD":   {"nombre": "Matemáticas Discretas",                        "cuatrimestre": 1, "prereqs": []},
    "PDS":  {"nombre": "Procesos de Desarrollo de Software",           "cuatrimestre": 1, "prereqs": []},

    # ── CUATRIMESTRE 2 ──────────────────────────────────────────────────────
    "POO":  {"nombre": "Programación Orientada a Objetos",             "cuatrimestre": 2, "prereqs": ["ALG"]},
    "ED":   {"nombre": "Estructura de Datos",                          "cuatrimestre": 2, "prereqs": ["ALG"]},
    "CI":   {"nombre": "Cálculo Integral",                             "cuatrimestre": 2, "prereqs": ["CD"]},
    "FBD":  {"nombre": "Fundamentos de Base de Datos",                 "cuatrimestre": 2, "prereqs": []},
    "IRS":  {"nombre": "Ingeniería de Requerimientos de Software",     "cuatrimestre": 2, "prereqs": ["PDS"]},

    # ── CUATRIMESTRE 3 ──────────────────────────────────────────────────────
    "PV":   {"nombre": "Programación Visual",                          "cuatrimestre": 3, "prereqs": ["POO"]},
    "EDA":  {"nombre": "Estructura de Datos Avanzadas",                "cuatrimestre": 3, "prereqs": ["ED"]},
    "MI1":  {"nombre": "Matemáticas para Ingeniería I",                "cuatrimestre": 3, "prereqs": ["CI"]},
    "BD":   {"nombre": "Base de Datos",                                "cuatrimestre": 3, "prereqs": ["FBD"]},
    "ISAC": {"nombre": "Ingeniería de Software Asistida por Computadora", "cuatrimestre": 3, "prereqs": ["IRS"]},

    # ── CUATRIMESTRE 4 ──────────────────────────────────────────────────────
    "PW":   {"nombre": "Programación Web",                             "cuatrimestre": 4, "prereqs": ["PV"]},
    "MI2":  {"nombre": "Matemáticas para Ingeniería II",               "cuatrimestre": 4, "prereqs": ["MI1"]},
    "AS":   {"nombre": "Arquitectura de Software",                     "cuatrimestre": 4, "prereqs": ["ISAC"]},
    "LA":   {"nombre": "Lenguajes y Autómatas",                        "cuatrimestre": 4, "prereqs": ["EDA"]},

    # ── CUATRIMESTRE 5 ──────────────────────────────────────────────────────
    "PCS":  {"nombre": "Programación Cliente/Servidor",                "cuatrimestre": 5, "prereqs": ["PW"]},
    "PE":   {"nombre": "Probabilidad y Estadística",                   "cuatrimestre": 5, "prereqs": ["MI2"]},
    "DI":   {"nombre": "Diseño de Interfaces",                         "cuatrimestre": 5, "prereqs": ["PW"]},
    "CS":   {"nombre": "Calidad del Software",                         "cuatrimestre": 5, "prereqs": ["AS"]},
    "CI2":  {"nombre": "Compiladores e Intérpretes",                   "cuatrimestre": 5, "prereqs": ["LA"]},

    # ── CUATRIMESTRE 6 ──────────────────────────────────────────────────────
    "PC":   {"nombre": "Programación Concurrente",                     "cuatrimestre": 6, "prereqs": ["PCS"]},
    "RED":  {"nombre": "Redes",                                        "cuatrimestre": 6, "prereqs": ["PCS"]},
    "MDD":  {"nombre": "Multimedia y Diseño Digital",                  "cuatrimestre": 6, "prereqs": ["DI"]},
    "PS":   {"nombre": "Pruebas del Software",                         "cuatrimestre": 6, "prereqs": ["CS"]},

    # ── CUATRIMESTRE 7 ──────────────────────────────────────────────────────
    "PM1":  {"nombre": "Programación para Móviles I",                  "cuatrimestre": 7, "prereqs": ["PC"]},
    "SO":   {"nombre": "Sistemas Operativos",                          "cuatrimestre": 7, "prereqs": ["RED"]},
    "IA":   {"nombre": "Inteligencia Artificial",                      "cuatrimestre": 7, "prereqs": ["PE", "MD"]},
    "MS":   {"nombre": "Mantenimiento de Software",                    "cuatrimestre": 7, "prereqs": ["PS"]},
    "MD2":  {"nombre": "Minería de Datos",                             "cuatrimestre": 7, "prereqs": ["BD", "PE"]},

    # ── CUATRIMESTRE 8 ──────────────────────────────────────────────────────
    "PM2":  {"nombre": "Programación para Móviles II",                 "cuatrimestre": 8, "prereqs": ["PM1"]},
    "SI":   {"nombre": "Seguridad de la Información",                  "cuatrimestre": 8, "prereqs": ["PM1"]},
    "AOS":  {"nombre": "Arquitectura Orientada a Servicios",           "cuatrimestre": 8, "prereqs": ["PC"]},
    "AFS":  {"nombre": "Análisis Financiero del Software",             "cuatrimestre": 8, "prereqs": ["MS"]},
    "APS":  {"nombre": "Administración de Proyectos de Software",      "cuatrimestre": 8, "prereqs": ["MS"]},

    # ── CUATRIMESTRE 9 — Estancia I ─────────────────────────────────────────
    "EST1": {"nombre": "Estancia I",                                   "cuatrimestre": 9,  "prereqs": ["PM2", "SI", "AOS", "IA", "MD2", "AFS", "APS"]},

    # ── CUATRIMESTRE 10 — META ──────────────────────────────────────────────
    "EST2": {"nombre": "Estancia II (META)",                           "cuatrimestre": 10, "prereqs": ["EST1"]},
}

# Conjunto completo de IDs
TODAS_LAS_MATERIAS: set = set(MATERIAS.keys())

# Estado meta: aprobar Estancia II
META: set = {"EST2"}


def materias_elegibles(aprobadas: frozenset, cuatrimestre_actual: int) -> list:
    """
    Devuelve los IDs de materias que el alumno puede cursar dado:
      - aprobadas          : conjunto de materias ya aprobadas
      - cuatrimestre_actual: cuatrimestre vigente del alumno

    Una materia es elegible si:
      1. No ha sido aprobada aún.
      2. Todos sus prerequisitos están aprobados.
      3. Su nivel de cuatrimestre es <= cuatrimestre_actual
         (se puede cursar una materia de nivel inferior en cualquier momento).
    """
    pendientes = TODAS_LAS_MATERIAS - aprobadas
    elegibles = []
    for mid in pendientes:
        m = MATERIAS[mid]
        prereqs_ok = all(p in aprobadas for p in m["prereqs"])
        nivel_ok = m["cuatrimestre"] <= cuatrimestre_actual
        if prereqs_ok and nivel_ok:
            elegibles.append(mid)
    return elegibles
