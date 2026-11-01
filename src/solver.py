"""
solver.py — Algoritmo UCS (Uniform-Cost Search) puro
Planificador de Trayectoria Académica — Ingeniería en Software

El estado es: (frozenset de materias aprobadas, cuatrimestre vigente)
El costo de un paso es: 1.0 + EPSILON * n_materias_en_accion
  - El término 1.0 minimiza cuatrimestres (objetivo primario).
  - El término EPSILON * n penaliza la carga excesiva (objetivo secundario).
"""

import heapq
import time
from functools import lru_cache
from itertools import combinations

from src.curriculum import MATERIAS, TODAS_LAS_MATERIAS, META, materias_elegibles

# ── Parámetros del solver ────────────────────────────────────────────────────
MAX_MATERIAS_POR_PERIODO = 9   # Carga máxima por cuatrimestre
EPSILON = 0.01                 # Penalización por materia adicional en un periodo
MAX_COMBOS_POR_NODO = 200      # Tope de acciones generadas en un nodo


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


def generar_acciones(elegibles: list) -> list:
    """
    Genera acciones (subconjuntos de materias elegibles a inscribir).

    Estrategia de poda y optimización:
      1. Ordena los elegibles dando prioridad a materias críticas (que desbloquean
         más materias posteriores), luego menor cuatrimestre original.
      2. Si el número de elegibles cabe dentro de la carga máxima (<= 9),
         se explora la carga completa y subconjuntos cercanos de alta carga
         para avanzar eficientemente sin retrasar la graduación ni crear
         caminos redundantes dominados.
    """
    if not elegibles:
        return []

    # Ordenar por criticidad descendente, luego nivel de cuatrimestre ascendente, y mid
    ordenados = sorted(
        elegibles,
        key=lambda m: (-_criticidad(m), MATERIAS[m]["cuatrimestre"], m)
    )

    if len(ordenados) <= MAX_MATERIAS_POR_PERIODO:
        acciones = [frozenset(ordenados)]
        if len(ordenados) > 1:
            for combo in combinations(ordenados, len(ordenados) - 1):
                acciones.append(frozenset(combo))
                if len(acciones) >= 25:
                    break
        return acciones

    # Si hay más de 9 elegibles:
    pool = ordenados[: min(len(ordenados), 11)]
    acciones = []
    for k in [MAX_MATERIAS_POR_PERIODO, MAX_MATERIAS_POR_PERIODO - 1]:
        for combo in combinations(pool, k):
            acciones.append(frozenset(combo))
            if len(acciones) >= 35:
                return acciones

    return acciones


def costo_paso(accion: frozenset) -> float:
    """
    Costo de tomar `accion` en un cuatrimestre:
      - 1.0  por periodo (minimizar cuatrimestres es el objetivo principal)
      - EPSILON * n_materias como desempate (favorece cargas más ligeras ante
        igual número de cuatrimestres)
    """
    return 1.0 + len(accion) * EPSILON


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
        Función opcional para reportar progreso; recibe un string con el
        estado del nodo que se está expandiendo.

    Retorna
    -------
    dict con claves:
        'plan'              : list[dict] — un dict por cuatrimestre con
                             'cuatrimestre', 'materias', 'nombres', 'costo_paso'
        'costo_total'       : float
        'cuatrimestres'     : int — número de periodos en el plan
        'nodos_expandidos'  : int
        'nodos_generados'   : int
        'tiempo_seg'        : float
    None si no existe solución.
    """
    t_inicio = time.time()

    # Estado inicial
    aprobadas_ini = frozenset(aprobadas_iniciales)
    estado_inicial = (aprobadas_ini, cuatrimestre_inicial)

    # Cola de prioridad: (costo_acumulado, contador_desempate, estado, plan)
    cola: list = []
    counter = 0
    heapq.heappush(cola, (0.0, counter, estado_inicial, []))

    # Registro de mejor costo conocido para cada estado
    visitados: dict = {}

    nodos_expandidos = 0
    nodos_generados = 1   # contamos el nodo inicial

    while cola:
        g, _, (aprobadas, cuatri), plan = heapq.heappop(cola)

        # Si ya procesamos este estado con igual o menor costo, descartamos
        estado_key = (aprobadas, cuatri)
        if estado_key in visitados and visitados[estado_key] <= g:
            continue
        visitados[estado_key] = g

        nodos_expandidos += 1

        if callback:
            callback(
                f"Expandiendo nodo {nodos_expandidos} | "
                f"g={g:.3f} | Cuatrimestre {cuatri} | "
                f"Aprobadas: {len(aprobadas)}/{len(TODAS_LAS_MATERIAS)}"
            )

        # ── Comprobación de meta ─────────────────────────────────────────────
        if es_meta(aprobadas):
            t_fin = time.time()
            return {
                "plan":             plan,
                "costo_total":      round(g, 4),
                "cuatrimestres":    len(plan),
                "nodos_expandidos": nodos_expandidos,
                "nodos_generados":  nodos_generados,
                "tiempo_seg":       round(t_fin - t_inicio, 4),
            }

        # ── Generación de sucesores ──────────────────────────────────────────
        elegibles = materias_elegibles(aprobadas, cuatri)

        if not elegibles:
            # Sin materias elegibles: avanzar al siguiente cuatrimestre
            # (el alumno "pierde" un periodo sin cursar nada)
            nuevo_estado = (aprobadas, cuatri + 1)
            nuevo_g = g + 1.0
            clave_nuevo = nuevo_estado
            if clave_nuevo not in visitados or visitados[clave_nuevo] > nuevo_g:
                counter += 1
                nodos_generados += 1
                heapq.heappush(cola, (nuevo_g, counter, nuevo_estado, plan))
            continue

        acciones = generar_acciones(elegibles)

        for accion in acciones:
            nuevas_aprobadas = aprobadas | accion
            nuevo_cuatri = cuatri + 1
            nuevo_g = g + costo_paso(accion)

            nuevo_estado = (nuevas_aprobadas, nuevo_cuatri)
            clave_nuevo = nuevo_estado

            # Poda: ignorar si ya conocemos un camino igual o mejor
            if clave_nuevo in visitados and visitados[clave_nuevo] <= nuevo_g:
                continue

            detalle = {
                "cuatrimestre": cuatri,
                "materias":     sorted(list(accion)),
                "nombres":      [MATERIAS[m]["nombre"] for m in sorted(accion)],
                "costo_paso":   round(costo_paso(accion), 4),
            }
            nueva_plan = plan + [detalle]

            counter += 1
            nodos_generados += 1
            heapq.heappush(cola, (nuevo_g, counter, nuevo_estado, nueva_plan))

    # Sin solución
    return None
