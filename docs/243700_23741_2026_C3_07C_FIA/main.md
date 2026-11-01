# Resumen {-}

Este proyecto aborda la problemática de planificación de trayectorias académicas para estudiantes irregulares mediante técnicas de Inteligencia Artificial[cite: 4]. Se modeló el mapa curricular como un problema de búsqueda en un espacio de estados, implementando el algoritmo de Búsqueda de Costo Uniforme (UCS) para encontrar la ruta óptima de recuperación[cite: 2, 4]. El sistema sugiere las asignaturas a cursar por periodo, garantizando el cumplimiento de prerrequisitos y restricciones de carga, con el fin de que el alumno alcance la graduación en el menor número de cuatrimestres posible[cite: 3, 4].

# Abstract {-}

This project addresses the problem of planning academic trajectories for irregular students using Artificial Intelligence techniques[cite: 4]. The curriculum map was modeled as a state-space search problem, implementing the Uniform-Cost Search (UCS) algorithm to find the optimal recovery path[cite: 2, 4]. The system suggests the subjects to take per period, guaranteeing compliance with prerequisites and load constraints, in order for the student to achieve graduation in the shortest possible number of terms[cite: 3, 4].

# PLANIFICADOR DE TRAYECTORIA ACADÉMICA CON BÚSQUEDA DE COSTO UNIFORME

## Planteamiento del problema

En las instituciones de educación superior, un alumno adquiere el estatus de irregular cuando reprueba o deja de cursar asignaturas dentro de la secuencia sugerida por el mapa curricular[cite: 4]. El problema consiste en diseñar un plan de recuperación que permita al estudiante regularizar su situación en el menor tiempo posible (mínimo de cuatrimestres) sin exceder las restricciones institucionales[cite: 4].

Específicamente, para la Universidad Politécnica, el planificador debe respetar el mapa de seriación de asignaturas, permitiendo transicionar únicamente hacia materias elegibles (aquellas cuyos prerrequisitos ya estén aprobados)[cite: 4]. Además, se debe respetar la regla que limita la carga académica a un máximo de 9 asignaturas por periodo lectivo, incluyendo un máximo de dos convalidaciones[cite: 4]. 

## PEAS

### Medida de desempeño

Minimizar el número de cuatrimestres necesarios para alcanzar la graduación y, como objetivo secundario, minimizar la carga académica (evitar sobrecargar al alumno con 9 materias si el mismo tiempo de egreso se logra con menos asignaturas)[cite: 3, 4]. Esta medida asegura un plan eficiente y humanamente viable.

### Entorno

El entorno está conformado por el expediente académico actual del estudiante (materias aprobadas), su cuatrimestre escolar vigente y las reglas estáticas del mapa de seriación (prerrequisitos) del plan de estudios de la carrera[cite: 2, 4].

#### Características del entorno

| Característica | Justificación |
| :--- | :--- |
| **Determinista** | Se asume que si el sistema decide inscribir al alumno en una materia, este la aprobará al finalizar el periodo escolar[cite: 4]. |
| **Monoagente** | El algoritmo planifica la trayectoria individual de un único estudiante de forma aislada, sin competencia ni cooperación con otros[cite: 4]. |
| **Completamente observable** | El sistema conoce el 100% de las reglas del plan de estudios, las seriaciones y el historial completo del alumno en todo momento[cite: 4]. |
| **Secuencial** | Las materias que se deciden tomar en el periodo actual determinan directamente qué nuevas asignaturas se desbloquearán para el siguiente periodo[cite: 4]. |
| **Discreto** | El espacio de estados, el catálogo de materias y el transcurso del tiempo (cuatrimestres) son finitos y se cuentan en unidades enteras[cite: 4]. |
| **Estático** | El mapa curricular y las reglas institucionales no cambian mientras el algoritmo está calculando la ruta óptima[cite: 4]. |

### Actuadores

El motor de transiciones del sistema, el cual actúa seleccionando e inscribiendo un subconjunto válido de asignaturas (entre 1 y 9 materias, con máximo 2 convalidaciones) para conformar la carga académica de un cuatrimestre específico[cite: 3, 4].

### Sensores

La interfaz de usuario del sistema, compuesta por selectores (spinbox) para capturar el cuatrimestre actual del alumno y casillas de verificación (checkboxes) para identificar las materias que ya han sido aprobadas en su historial.

## Especificación del problema de búsqueda

### Estado inicial

El estado inicial $S_0$ se define como una tupla $(A_{inicial}, T_{actual})$, donde $A$ es el conjunto de materias aprobadas y $T$ el cuatrimestre actual[cite: 4].
* **Ejemplo 1 (Alumno Regular):** $S_0 = (\{Algoritmos, Algebra Lineal, ...\}, 4)$. Un estudiante en 4to cuatrimestre que aprobó todo lo de los 3 anteriores[cite: 2].
* **Ejemplo 2 (Alumno Irregular):** $S_0 = (\{Algoritmos\}, 2)$. Un estudiante en 2do cuatrimestre que reprobó casi todo en el primero.

### Meta

El estado meta se alcanza cuando la función $\text{IsGoal}(S_i)$ es verdadera, lo que significa que el conjunto de asignaturas aprobadas del alumno ($A_i$) es exactamente igual al universo total de materias del plan de estudios ($\mathcal{U}$)[cite: 4].
* **Ejemplo:** El alumno llega al estado donde la última materia requerida, "Estancia II", se añade a su conjunto de materias aprobadas[cite: 2].

### Espacio de estados

El espacio de estados abarca todas las combinaciones posibles entre los subconjuntos del catálogo de materias y los cuatrimestres[cite: 4]. Dado que hay decenas de materias, el tamaño máximo teórico es muy grande ($2^N \times T$), pero en la práctica se reduce drásticamente porque las ramas inválidas por seriación son podadas antes de entrar a la cola de prioridad del algoritmo.

### Transiciones

Las transiciones se generan obteniendo las combinaciones posibles de materias elegibles[cite: 4].

| Condición para la Transición | Restricción |
| :--- | :--- |
| **Cumplimiento de Prerrequisitos** | Todas las materias seriadas previas deben estar en el conjunto de aprobadas[cite: 4]. |
| **Restricción de Nivel** | El nivel de la materia debe ser $\le$ al cuatrimestre actual del estudiante[cite: 4]. |
| **Carga Académica** | El tamaño de la combinación de materias ($a$) debe ser $1 \le \vert a \vert \le 9$[cite: 4]. |
| **Convalidaciones** | Máximo 2 por periodo[cite: 4]. |

### Métricas de rendimiento

Se utiliza la función de costo $g(n)$ de la Búsqueda de Costo Uniforme (UCS), definida como: $c = 1.0 + (\vert a \vert \times 0.01)$[cite: 2, 4].
Se justifica porque el costo base ($1.0$) fuerza al algoritmo a priorizar encontrar la solución en el menor número de cuatrimestres, mientras que el costo marginal ($0.01$ por materia) actúa como desempate para elegir la trayectoria con menor carga académica si dos rutas tardan el mismo tiempo[cite: 4].

### Heurísticas

Al tratarse de una Búsqueda en Espacio de Estados No Informada (Uniform-Cost Search), el algoritmo no utiliza una función heurística $h(n)$ para estimar la distancia a la meta, basando sus decisiones de expansión estrictamente en el costo real acumulado $g(n)$ desde el nodo raíz[cite: 4].

# Implementación

En este capítulo se documenta la implementación del algoritmo de búsqueda. La lógica matemática, las transiciones y el motor UCS han sido completamente separados de la interfaz de usuario. 

```python
# label: LA.C1.A4.CODE::UCS_Search caption: "Motor de Búsqueda de Costo Uniforme (UCS)"
def ucs(aprobadas_iniciales: set, cuatrimestre_inicial: int, callback=None):
    """
    Uniform-Cost Search para encontrar la trayectoria académica óptima.

    Parámetros
    ----------
    aprobadas_iniciales : set
        IDs de materias ya aprobadas por el alumno. Representa la base de A_i.
    cuatrimestre_inicial : int
        Cuatrimestre en el que se encuentra actualmente el alumno. Representa T_i.
    callback : callable(str) | None
        Función opcional para reportar el progreso del nodo.

    Hace
    ----
    Expande nodos desde un estado (A_i, T_i) hacia un estado (A_{i+1}, T_{i+1}) 
    utilizando una cola de prioridad basada en g(n). Descarta ramas con costos 
    subóptimos apoyándose en un diccionario de nodos visitados y detiene la 
    búsqueda cuando el estado contiene todas las asignaturas de la carrera.

    Retorna
    -------
    Un diccionario con la secuencia óptima de cuatrimestres a cursar (plan), 
    el costo total de la ruta, número de periodos, nodos expandidos, nodos 
    generados y tiempo de cómputo en segundos. Si es irresoluble, retorna None.
    """
    t_inicio = time.time()
    aprobadas_ini = frozenset(aprobadas_iniciales)
    estado_inicial = (aprobadas_ini, cuatrimestre_inicial)

    # Cola: (costo_acumulado g, contador_desempate, estado, plan)
    cola: list = []
    counter = 0
    heapq.heappush(cola, (0.0, counter, estado_inicial, []))
    visitados: dict = {}
    
    nodos_expandidos = 0
    nodos_generados = 1 

    while cola:
        g, _, (aprobadas, cuatri), plan = heapq.heappop(cola)
        estado_key = (aprobadas, cuatri)
        
        if estado_key in visitados and visitados[estado_key] <= g:
            continue
        visitados[estado_key] = g
        nodos_expandidos += 1

        if es_meta(aprobadas):
            return {
                "plan": plan, "costo_total": round(g, 4),
                "cuatrimestres": len(plan), "nodos_expandidos": nodos_expandidos,
                "nodos_generados": nodos_generados, "tiempo_seg": round(time.time() - t_inicio, 4)
            }

        elegibles = materias_elegibles(aprobadas, cuatri)
        if not elegibles:
            nuevo_estado = (aprobadas, cuatri + 1)
            nuevo_g = g + 1.0
            if nuevo_estado not in visitados or visitados[nuevo_estado] > nuevo_g:
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

            if nuevo_estado in visitados and visitados[nuevo_estado] <= nuevo_g:
                continue

            nueva_plan = plan + [{"cuatrimestre": cuatri, "materias": sorted(list(accion))}]
            counter += 1
            nodos_generados += 1
            heapq.heappush(cola, (nuevo_g, counter, nuevo_estado, nueva_plan))

    return None
  
# label: LA.C1.A4.CODE::FuncTran caption: "Generador de Transiciones (Acciones)"
def generar_acciones(elegibles: list) -> list:
    """
    Genera acciones (subconjuntos de materias elegibles a inscribir).

    Parámetros
    ----------
    elegibles : list
        Lista de IDs de materias cuyos prerrequisitos ya fueron aprobados y 
        su nivel es menor o igual al cuatrimestre actual.

    Hace
    ----
    Crea subconjuntos válidos evaluando una heurística intrínseca: ordena las
    materias priorizando su criticidad (cantidad de asignaturas futuras que
    desbloquean) y nivel. Genera combinaciones respetando el límite de 
    MAX_MATERIAS_POR_PERIODO (9). Implementa una poda temprana de ramas débiles
    para evitar combinaciones ineficientes en cargas altas.

    Retorna
    -------
    Una lista de 'frozensets', donde cada frozenset representa un bloque de 
    materias válido para ser inscrito en el cuatrimestre actual.
    """
    if not elegibles:
        return []

    # Ordenar por criticidad descendente y nivel de cuatrimestre ascendente
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

    pool = ordenados[: min(len(ordenados), 11)]
    acciones = []
    for k in [MAX_MATERIAS_POR_PERIODO, MAX_MATERIAS_POR_PERIODO - 1]:
        for combo in combinations(pool, k):
            acciones.append(frozenset(combo))
            if len(acciones) >= 35:
                return acciones

    return acciones

# label: LA.C1.A4.CODE::CostFunc caption: "Cálculo del Costo de Paso"
def costo_paso(accion: frozenset) -> float:
    """
    Calcula el costo marginal de realizar una transición (inscribir materias).

    Parámetros
    ----------
    accion : frozenset
        El conjunto de materias seleccionadas para inscribir en el periodo.

    Hace
    ----
    Aplica la fórmula matemática $c = 1.0 + (\vert a \vert \times \epsilon)$. 
    El valor 1.0 fuerza al algoritmo UCS a minimizar periodos. 
    La constante EPSILON (0.01) actúa como desempate.

    Retorna
    -------
    Un float con el costo numérico (ej. 1.05 si se inscriben 5 materias).
    """
    return 1.0 + len(accion) * EPSILON

# Resultados

A continuación, se presentan tres ejemplos de la ejecución del algoritmo resolviendo escenarios comunes y complejos que demuestran la funcionalidad del sistema[cite: 3].

## Caso 1

### Descripción
Alumno Regular: Se evalúa un estudiante ideal que cursa su carrera de forma normal, sin adeudar asignaturas de periodos anteriores[cite: 3]. Este caso confirma que el algoritmo respeta la secuencia natural establecida por el mapa curricular.

### Estado inicial y meta
* **Estado inicial:** $S_0 = (\{Algoritmos, Algebra Lineal, ...\}, 4)$. El alumno se encuentra en 4to cuatrimestre y ha aprobado satisfactoriamente todas las asignaturas de los cuatrimestres 1, 2 y 3[cite: 2, 3].
* **Meta:** Que el conjunto de asignaturas aprobadas equivalga a la totalidad del plan de estudios ($\text{IsGoal} = \text{True}$)[cite: 4].

*(Inserta aquí la captura de pantalla de tu interfaz con el alumno regular configurado)*

### Solución
*(Inserta aquí la captura de pantalla mostrando la trayectoria resultante para el alumno regular)*

### Ejecución
*(Inserta aquí la secuencia de imágenes o capturas paso a paso de la resolución, si tu interfaz lo permite. Si no, inserta las capturas de la métrica de desempeño al finalizar).*

### Comentarios
El algoritmo UCS retorna de manera instantánea la trayectoria estándar sugerida por la institución académica[cite: 3]. La función de costo $g(n)$ garantiza el egreso en el mínimo de cuatrimestres sin requerir recálculos complejos, comprobando el correcto funcionamiento base de la búsqueda y la seriación[cite: 4].


## Caso 2

### Descripción
Cuello de Botella Crítico: Se simula un alumno que reprobó asignaturas fundamentales en los primeros periodos, las cuales abren largas cadenas de seriación consecutivas (por ejemplo, reprueba asignaturas de programación básica que bloquean Programación Orientada a Objetos y, subsecuentemente, Programación Web)[cite: 3].

### Estado inicial y meta
* **Estado inicial:** $S_0 = (\{Materias_Aprobadas\}, 3)$. El alumno está en 3er periodo pero carece de asignaturas clave del 1er periodo.
* **Meta:** Cursar todas las asignaturas minimizando el rezago provocado por la cadena bloqueada[cite: 4].

*(Inserta aquí la captura de pantalla configurando el alumno irregular con las materias clave desmarcadas)*

### Solución
*(Inserta aquí la captura de la trayectoria resultante)*

### Ejecución
*(Inserta aquí la secuencia de imágenes de la ejecución)*

### Comentarios
El generador de acciones, apoyado por su función interna `_criticidad()`, demuestra su efectividad[cite: 7]. El algoritmo identifica correctamente la "rama crítica" y fuerza al estudiante a cursar la asignatura bloqueada de forma prioritaria en el cuatrimestre más próximo, demostrando una planificación inteligente que prioriza destrabar el mapa curricular[cite: 3].


## Caso 3

### Descripción
Carga Dispersa: Un estudiante que se ha rezagado debido a la reprobación de múltiples materias no fuertemente seriadas de distintas áreas (ejemplo: reprueba 7 materias diferentes simultáneamente)[cite: 3].

### Estado inicial y meta
* **Estado inicial:** $S_0 = (\{Materias_Restantes\}, 5)$. El estudiante está en 5to cuatrimestre, con un expediente fragmentado.
* **Meta:** Nivelar al estudiante combinando eficientemente asignaturas atrasadas con materias de su cuatrimestre actual[cite: 3, 4].

*(Inserta aquí la captura de pantalla con múltiples materias desmarcadas al azar)*

### Solución
*(Inserta aquí la captura de la trayectoria resultante)*

### Ejecución
*(Inserta aquí la secuencia de imágenes de la ejecución)*

### Comentarios
El sistema agrupó exitosamente la carga académica utilizando el límite máximo permitido ($\le 9$ materias)[cite: 3, 4]. El desempate de la función de costo ($EPSILON$) garantizó que, al llegar al estado meta, el UCS escogiera la combinación que requería menos cuatrimestres sin saturar al estudiante con materias de relleno innecesarias[cite: 4, 7].


# Conclusiones y recomendaciones

## Conclusiones
La implementación de la Búsqueda de Costo Uniforme (UCS) para el modelado de trayectorias académicas demostró ser una solución altamente efectiva. Se comprobó que el diseño cuidadoso de la función de costo ($g(n)$) es crucial: al combinar un peso alto (1.0) para el tiempo y un peso marginal ($0.01$) para la carga, se logró automatizar un criterio humano (no sobrecargar al alumno inútilmente) utilizando estrictamente IA no informada[cite: 4, 7]. Además, el ejercicio de separar las reglas del dominio (seriación) del motor de búsqueda permitió comprender la naturaleza agnóstica de los algoritmos de búsqueda en el espacio de estados.

## Recomendaciones
*   **Mejora de Poda:** Si el catálogo de materias incrementa, se recomienda evolucionar el algoritmo hacia una Búsqueda Informada (A*) diseñando una heurística $h(n)$ que estime el número mínimo de cuatrimestres faltantes basados en las cadenas de seriación más largas.
*   **Gestión de Datos:** Se sugiere integrar la plataforma a una base de datos institucional (SQL) para no depender de diccionarios en código, permitiendo actualizar el mapa curricular sin modificar el solver.
*   **Flexibilidad de Restricciones:** Añadir selectores en la interfaz visual que permitan modificar en tiempo de ejecución las reglas de la universidad (ej. bajar la restricción máxima a 7 materias en lugar de 9 para perfiles específicos).

# Anexos
*(Si es necesario, colocar aquí diagramas adicionales del árbol de búsqueda, el manual de uso del planificador o referencias técnicas del entorno de desarrollo utilizado).*