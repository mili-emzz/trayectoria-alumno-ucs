"""
solver.py — Algoritmo UCS (Uniform-Cost Search) puro
Planificador de Trayectoria Académica — Ingeniería en Tecnologías de la Información
e Innovación Digital (IT2iD)

El estado es: (frozenset de materias aprobadas, cuatrimestre vigente)

Dos metas encadenadas (restricciones estrictas):
  META 1: aprobar TODO Q1-Q5  -> habilita la Estadía TSU (EST_TSU).
  META 2: aprobar EST_TSU y TODO Q7-Q9 -> habilita la Estadía profesional (EST_IT2ID).
Por lo tanto: ninguna materia de Q7-Q9 se cursa antes de aprobar EST_TSU, y
EST_IT2ID es siempre lo último. Las estadías se cursan SOLAS en su cuatrimestre.

El costo de un paso es una TUPLA que se compara de forma lexicográfica:

    costo_paso = (1, retraso, carga²)

  1. periodos : 1 por cuatrimestre (objetivo primario: menor número de cuatrimestres).
  2. retraso  : Σ (cuatrimestre en que se cursa - nivel de la materia). Un alumno
                regular tiene retraso 0 y sigue su plan normal.
  3. carga²   : Σ |acción|². Desempate: reparte la carga de forma pareja.
(Con un ε lineal `1 + ε·n` la suma de penalizaciones es siempre ε × materias
pendientes, igual para cualquier plan con los mismos periodos: no desempata.)
"""

import heapq
import time
from functools import lru_cache
from itertools import combinations

from src.curriculum import MATERIAS, TODAS_LAS_MATERIAS, META, materias_elegibles

# ── Parámetros del solver ────────────────────────────────────────────────────
MAX_MATERIAS_POR_PERIODO = 9   # Carga máxima por cuatrimestre
EPSILON = 0.01                 # Solo para mostrar `costo_total` (la búsqueda usa tuplas)
MAX_COMBOS_POR_NODO = 35       # Tope de acciones generadas en un nodo
LIMITE_CUATRIMESTRES = 30      # Seguridad: evita búsquedas infinitas si no hay solución

# ── Estructura de las dos metas ──────────────────────────────────────────────
EST_TSU = "EST_TSU"
EST_PROF = "EST_IT2ID"
ESTADIAS = frozenset({EST_TSU, EST_PROF})   # Se cursan solas
BLOQUE_TSU = frozenset(m for m, d in MATERIAS.items() if d["cuatrimestre"] <= 5)
BLOQUE_ING = frozenset(m for m, d in MATERIAS.items() if 7 <= d["cuatrimestre"] <= 9)


@lru_cache(maxsize=None)
def _criticidad(mid: str) -> int:
    """
    Cuenta (con caché) cuántas materias dependen transitivamente de `mid`.
    Un valor más alto => la materia desbloquea más caminos hacia la meta.
    """
    count = 0
    for m2, data in MATERIAS.items():
        if mid in data["prereqs"]:
            count += 1 + _criticidad(m2)
    return count


def elegibles_estrictas(aprobadas: frozenset, cuatrimestre: int) -> list:
    """
    Materias elegibles según el catálogo (prerequisitos y nivel) MÁS las
    restricciones de las dos metas:
      - EST_TSU solo si están aprobadas todas las materias de Q1-Q5.
      - Las materias de Q7-Q9 solo después de aprobar EST_TSU.
      - EST_IT2ID solo si están aprobadas EST_TSU y todas las de Q7-Q9.
    """
    tsu_ok = EST_TSU in aprobadas
    resultado = []
    for m in materias_elegibles(aprobadas, cuatrimestre):
        if m == EST_TSU and not BLOQUE_TSU <= aprobadas:
            continue
        if m == EST_PROF and not (tsu_ok and BLOQUE_ING <= aprobadas):
            continue
        if m in BLOQUE_ING and not tsu_ok:
            continue
        resultado.append(m)
    return resultado


def _acciones_regulares(elegibles: list) -> list:
    """
    Acciones sobre materias que NO son estadías (estrategia amplia del original).

      1. Ordena los elegibles dando prioridad a materias críticas (que desbloquean
         más materias posteriores), luego menor cuatrimestre original.
      2. Si caben en la carga máxima (<= 9): la carga completa y los subconjuntos
         que omiten una materia.
      3. Si hay más de 9: subconjuntos de 9 y de 8 materias del `pool` prioritario.
    """
    ordenados = sorted(
        elegibles,
        key=lambda m: (-_criticidad(m), MATERIAS[m]["cuatrimestre"], m)
    )

    if len(ordenados) <= MAX_MATERIAS_POR_PERIODO:
        acciones = [frozenset(ordenados)]
        if len(ordenados) > 1:
            for combo in combinations(ordenados, len(ordenados) - 1):
                acciones.append(frozenset(combo))
                if len(acciones) >= MAX_COMBOS_POR_NODO:
                    break
        return acciones

    pool = ordenados[: min(len(ordenados), 11)]
    acciones = []
    for k in [MAX_MATERIAS_POR_PERIODO, MAX_MATERIAS_POR_PERIODO - 1]:
        for combo in combinations(pool, k):
            acciones.append(frozenset(combo))
            if len(acciones) >= MAX_COMBOS_POR_NODO:
                return acciones
    return acciones


def generar_acciones(elegibles: list) -> list:
    """
    Genera acciones (subconjuntos de materias elegibles a inscribir).
    Cada estadía elegible es una acción por sí sola (se cursa en exclusiva);
    las demás materias se agrupan según `_acciones_regulares`.
    """
    if not elegibles:
        return []

    estadias = sorted(m for m in elegibles if m in ESTADIAS)
    resto = sorted(m for m in elegibles if m not in ESTADIAS)

    acciones = [frozenset({e}) for e in estadias]
    if resto:
        acciones.extend(_acciones_regulares(resto))
    return acciones


def costo_paso(accion: frozenset, cuatrimestre: int) -> tuple:
    """Costo de tomar `accion` en `cuatrimestre`: (1, retraso, carga²)."""
    retraso = sum(cuatrimestre - MATERIAS[m]["cuatrimestre"] for m in accion)
    return (1, retraso, len(accion) ** 2)


def _sumar(g: tuple, c: tuple) -> tuple:
    return (g[0] + c[0], g[1] + c[1], g[2] + c[2])


def es_meta(aprobadas: frozenset) -> bool:
    """Devuelve True si todas las materias de META están aprobadas."""
    return META.issubset(aprobadas)


def ucs(aprobadas_iniciales: set, cuatrimestre_inicial: int, callback=None):
    """
    Uniform-Cost Search para encontrar la trayectoria académica óptima.

    Parámetros
    ----------
    aprobadas_iniciales : set
        IDs de materias ya aprobadas por el alumno.
    cuatrimestre_inicial : int
        Cuatrimestre en el que se encuentra actualmente el alumno.
    callback : callable(str) | None
        Función opcional para reportar progreso.

    Retorna
    -------
    dict con claves:
        'plan'              : list[dict] — un dict por cuatrimestre con
                             'cuatrimestre', 'materias', 'nombres', 'costo_paso'
        'costo_total'       : float — periodos + EPSILON·retraso (solo informativo)
        'cuatrimestres'     : int — número de periodos en el plan
        'retraso_total'     : int — Σ (cuatrimestre cursado - nivel) de todas las materias
        'nodos_expandidos'  : int
        'nodos_generados'   : int
        'tiempo_seg'        : float
    None si no existe solución.
    """
    t_inicio = time.time()

    aprobadas_ini = frozenset(aprobadas_iniciales)
    estado_inicial = (aprobadas_ini, cuatrimestre_inicial)

    # Cola de prioridad: (costo_acumulado (tupla), contador_desempate, estado, plan)
    cola: list = []
    counter = 0
    heapq.heappush(cola, ((0, 0, 0), counter, estado_inicial, []))

    visitados: dict = {}   # mejor costo conocido por estado

    nodos_expandidos = 0
    nodos_generados = 1

    while cola:
        g, _, (aprobadas, cuatri), plan = heapq.heappop(cola)

        estado_key = (aprobadas, cuatri)
        if estado_key in visitados and visitados[estado_key] <= g:
            continue
        visitados[estado_key] = g

        nodos_expandidos += 1

        if callback:
            callback(
                f"Expandiendo nodo {nodos_expandidos} | "
                f"periodos={g[0]} retraso={g[1]} | Cuatrimestre {cuatri} | "
                f"Aprobadas: {len(aprobadas)}/{len(TODAS_LAS_MATERIAS)}"
            )

        # ── Comprobación de meta ─────────────────────────────────────────────
        if es_meta(aprobadas):
            t_fin = time.time()
            return {
                "plan":             plan,
                "costo_total":      round(g[0] + EPSILON * g[1], 4),
                "cuatrimestres":    g[0],
                "retraso_total":    g[1],
                "nodos_expandidos": nodos_expandidos,
                "nodos_generados":  nodos_generados,
                "tiempo_seg":       round(t_fin - t_inicio, 4),
            }

        if cuatri >= cuatrimestre_inicial + LIMITE_CUATRIMESTRES:
            continue

        # ── Generación de sucesores ──────────────────────────────────────────
        elegibles = elegibles_estrictas(aprobadas, cuatri)

        if not elegibles:
            # Sin materias elegibles: el alumno "pierde" un periodo sin cursar nada
            nuevo_estado = (aprobadas, cuatri + 1)
            nuevo_g = _sumar(g, (1, 0, 0))
            if nuevo_estado not in visitados or visitados[nuevo_estado] > nuevo_g:
                detalle = {"cuatrimestre": cuatri, "materias": [], "nombres": [],
                           "costo_paso": (1, 0, 0)}
                counter += 1
                nodos_generados += 1
                heapq.heappush(cola, (nuevo_g, counter, nuevo_estado, plan + [detalle]))
            continue

        for accion in generar_acciones(elegibles):
            nuevo_estado = (aprobadas | accion, cuatri + 1)
            c = costo_paso(accion, cuatri)
            nuevo_g = _sumar(g, c)

            # Poda: ignorar si ya conocemos un camino igual o mejor
            if nuevo_estado in visitados and visitados[nuevo_estado] <= nuevo_g:
                continue

            detalle = {
                "cuatrimestre": cuatri,
                "materias":     sorted(list(accion)),
                "nombres":      [MATERIAS[m]["nombre"] for m in sorted(accion)],
                "costo_paso":   c,
            }

            counter += 1
            nodos_generados += 1
            heapq.heappush(cola, (nuevo_g, counter, nuevo_estado, plan + [detalle]))

    return None   # Sin solución
