"""
curriculum.py — Catálogo de materias y grafo de prerequisitos
Ingeniería en Tecnologías de la Información e Innovación Digital (IT2iD) — Planificador de Trayectoria Académica
"""

# ---------------------------------------------------------------------------
# Catálogo completo de materias
# Cada entrada tiene:
#   nombre      : nombre legible de la materia
#   cuatrimestre: nivel en el plan (1-10)
#   prereqs     : lista de IDs que deben estar aprobados antes
#
# Notas del plan IT2iD:
#   - Inglés I-VIII forman una cadena lineal (cada nivel solo depende del anterior).
#   - EST_TSU (Q6) y EST_IT2ID (Q10) son compuertas: requieren aprobar TODAS las
#     materias de Q1-Q5 y de Q7-Q9, respectivamente.
#   - FPT depende de PI2 (en el diagrama es una línea punteada; aquí se trata
#     como prerequisito normal).
#   - Q6 y Q10 contienen una sola materia (la estadía).
# ---------------------------------------------------------------------------
MATERIAS = {
    # ── CUATRIMESTRE 1 (sin prerequisitos) ────────────────────────────────
    "COM":      {"nombre": "Comunicación y Habilidades Digitales", "cuatrimestre": 1, "prereqs": []},
    "DHV":      {"nombre": "Desarrollo Humano y Valores", "cuatrimestre": 1, "prereqs": []},
    "FIS":      {"nombre": "Física", "cuatrimestre": 1, "prereqs": []},
    "FP":       {"nombre": "Fundamentos de Programación", "cuatrimestre": 1, "prereqs": []},
    "FR":       {"nombre": "Fundamentos de Redes", "cuatrimestre": 1, "prereqs": []},
    "FM":       {"nombre": "Fundamentos Matemáticos", "cuatrimestre": 1, "prereqs": []},
    "ING1":     {"nombre": "Inglés I", "cuatrimestre": 1, "prereqs": []},

    # ── CUATRIMESTRE 2 ────────────────────────────────────────────────────
    "CD":       {"nombre": "Cálculo Diferencial", "cuatrimestre": 2, "prereqs": ["FM"]},
    "CER":      {"nombre": "Conmutación y Enrutamiento de Redes", "cuatrimestre": 2, "prereqs": ["FR"]},
    "HSE":      {"nombre": "Habilidades Socioemocionales y Manejo de Conflictos", "cuatrimestre": 2, "prereqs": []},
    "ING2":     {"nombre": "Inglés II", "cuatrimestre": 2, "prereqs": ["ING1"]},
    "PE":       {"nombre": "Probabilidad y Estadística", "cuatrimestre": 2, "prereqs": ["FM"]},
    "PRE":      {"nombre": "Programación Estructurada", "cuatrimestre": 2, "prereqs": ["FP"]},
    "SO":       {"nombre": "Sistemas Operativos", "cuatrimestre": 2, "prereqs": ["FP"]},

    # ── CUATRIMESTRE 3 ────────────────────────────────────────────────────
    "BD":       {"nombre": "Bases de Datos", "cuatrimestre": 3, "prereqs": ["PRE"]},
    "CI":       {"nombre": "Cálculo Integral", "cuatrimestre": 3, "prereqs": ["CD"]},
    "DPT":      {"nombre": "Desarrollo del Pensamiento y Toma de Decisiones", "cuatrimestre": 3, "prereqs": []},
    "ING3":     {"nombre": "Inglés III", "cuatrimestre": 3, "prereqs": ["ING2"]},
    "POO":      {"nombre": "Programación Orientada a Objetos", "cuatrimestre": 3, "prereqs": ["PRE"]},
    "PI1":      {"nombre": "Proyecto Integrador I", "cuatrimestre": 3, "prereqs": []},
    "TCS":      {"nombre": "Tópicos de Calidad para el Diseño de Software", "cuatrimestre": 3, "prereqs": ["COM"]},

    # ── CUATRIMESTRE 4 ────────────────────────────────────────────────────
    "ADS":      {"nombre": "Análisis y Diseño de Software", "cuatrimestre": 4, "prereqs": ["POO", "TCS"]},
    "AW":       {"nombre": "Aplicaciones Web", "cuatrimestre": 4, "prereqs": ["POO"]},
    "CVV":      {"nombre": "Cálculo de Varias Variables", "cuatrimestre": 4, "prereqs": ["CI"]},
    "DAM":      {"nombre": "Desarrollo de Aplicaciones Móviles", "cuatrimestre": 4, "prereqs": ["POO"]},
    "ED":       {"nombre": "Estructura de Datos", "cuatrimestre": 4, "prereqs": ["POO"]},
    "EP":       {"nombre": "Ética Profesional", "cuatrimestre": 4, "prereqs": []},
    "ING4":     {"nombre": "Inglés IV", "cuatrimestre": 4, "prereqs": ["ING3"]},

    # ── CUATRIMESTRE 5 ────────────────────────────────────────────────────
    "AWS":      {"nombre": "Aplicaciones Web Orientadas a Servicios", "cuatrimestre": 5, "prereqs": ["AW", "BD"]},
    "BDA":      {"nombre": "Bases de Datos Avanzadas", "cuatrimestre": 5, "prereqs": ["BD"]},
    "EDO":      {"nombre": "Ecuaciones Diferenciales", "cuatrimestre": 5, "prereqs": ["CVV"]},
    "EMS":      {"nombre": "Estándares y Métricas para el Desarrollo de Software", "cuatrimestre": 5, "prereqs": ["ADS"]},
    "ING5":     {"nombre": "Inglés V", "cuatrimestre": 5, "prereqs": ["ING4"]},
    "LEAD":     {"nombre": "Liderazgo de Equipos de Alto Desempeño", "cuatrimestre": 5, "prereqs": []},
    "PI2":      {"nombre": "Proyecto Integrador II", "cuatrimestre": 5, "prereqs": ["PI1", "ADS"]},

    # ── CUATRIMESTRE 6 — Estadía TSU (requiere aprobar todo Q1-Q5) ────────
    "EST_TSU":  {"nombre": "Estadía TSU", "cuatrimestre": 6,
                 "prereqs": ["COM", "DHV", "FIS", "FP", "FR", "FM", "ING1", "CD", "CER", "HSE", "ING2",
                           "PE", "PRE", "SO", "BD", "CI", "DPT", "ING3", "POO", "PI1", "TCS", "ADS", "AW",
                           "CVV", "DAM", "ED", "EP", "ING4", "AWS", "BDA", "EDO", "EMS", "ING5", "LEAD",
                           "PI2"]},

    # ── CUATRIMESTRE 7 ────────────────────────────────────────────────────
    "BDN":      {"nombre": "Bases de Datos en la Nube (Optativa 1)", "cuatrimestre": 7, "prereqs": ["BDA"]},
    "ELTI":     {"nombre": "Ética y Legislación en Tecnologías de la Información", "cuatrimestre": 7, "prereqs": []},
    "FPT":      {"nombre": "Formulación de Proyectos de Tecnología", "cuatrimestre": 7, "prereqs": ["PI2"]},
    "FIA":      {"nombre": "Fundamentos de Inteligencia Artificial", "cuatrimestre": 7, "prereqs": ["PE", "ED", "BDA"]},
    "HG":       {"nombre": "Habilidades Gerenciales", "cuatrimestre": 7, "prereqs": []},
    "ING6":     {"nombre": "Inglés VI", "cuatrimestre": 7, "prereqs": ["ING5"]},
    "SEG":      {"nombre": "Seguridad Informática", "cuatrimestre": 7, "prereqs": ["CER", "SO"]},

    # ── CUATRIMESTRE 8 ────────────────────────────────────────────────────
    "ASV":      {"nombre": "Administración de Servidores", "cuatrimestre": 8, "prereqs": ["SO"]},
    "ELD":      {"nombre": "Electrónica Digital", "cuatrimestre": 8, "prereqs": ["FIS"]},
    "GPT":      {"nombre": "Gestión de Proyectos de Tecnología", "cuatrimestre": 8, "prereqs": ["FPT"]},
    "IF":       {"nombre": "Informática Forense", "cuatrimestre": 8, "prereqs": ["SEG", "SO"]},
    "ING7":     {"nombre": "Inglés VII", "cuatrimestre": 8, "prereqs": ["ING6"]},
    "PMA":      {"nombre": "Programación Móvil Avanzada (Optativa 2)", "cuatrimestre": 8, "prereqs": ["DAM"]},
    "PIA":      {"nombre": "Programación para Inteligencia Artificial", "cuatrimestre": 8, "prereqs": ["FIA"]},

    # ── CUATRIMESTRE 9 ────────────────────────────────────────────────────
    "CDA":      {"nombre": "Ciencia de Datos", "cuatrimestre": 9, "prereqs": ["PIA", "BDN"]},
    "EPT":      {"nombre": "Evaluación de Proyectos de Tecnología", "cuatrimestre": 9, "prereqs": ["GPT"]},
    "FMP":      {"nombre": "Frameworks para el Desarrollo Multiplataforma (Optativa 3)", "cuatrimestre": 9, "prereqs": ["AW", "PMA"]},
    "ING8":     {"nombre": "Inglés VIII", "cuatrimestre": 9, "prereqs": ["ING7"]},
    "IOT":      {"nombre": "Internet de las Cosas", "cuatrimestre": 9, "prereqs": ["ELD", "CER", "ED"]},
    "PI3":      {"nombre": "Proyecto Integrador III", "cuatrimestre": 9, "prereqs": ["GPT", "EMS"]},
    "TD":       {"nombre": "Tecnologías Disruptivas", "cuatrimestre": 9, "prereqs": ["PIA", "ELD"]},

    # ── CUATRIMESTRE 10 — META (requiere aprobar todo Q7-Q9) ──────────────
    "EST_IT2ID":{"nombre": "Estadía IT2iD", "cuatrimestre": 10,
                 "prereqs": ["BDN", "ELTI", "FPT", "FIA", "HG", "ING6", "SEG", "ASV", "ELD", "GPT", "IF",
                           "ING7", "PMA", "PIA", "CDA", "EPT", "FMP", "ING8", "IOT", "PI3", "TD"]},
}

# Conjunto completo de IDs
TODAS_LAS_MATERIAS: set = set(MATERIAS.keys())

# Estado meta: haber aprobado la totalidad de las materias del plan de estudios (100%),
# incluidas las dos estadías (EST_TSU y EST_IT2ID)
META: set = TODAS_LAS_MATERIAS


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