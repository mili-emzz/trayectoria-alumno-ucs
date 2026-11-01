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

```python
# label: LA.C1.A4.CODE::UCS_Search caption: "Motor de Búsqueda UCS para Trayectorias"
def uniform_cost_search(estado_inicial, plan_estudios):
    """
    Ejecuta el algoritmo de Búsqueda de Costo Uniforme (UCS).
    Recibe: 
      - estado_inicial: Tupla con (materias_aprobadas, cuatrimestre_actual).
      - plan_estudios: Grafo con la seriación curricular.
    Hace: 
      Expande nodos basándose en el costo acumulado g(n) = 1.0 + (materias * 0.01).
      Verifica transiciones válidas según prerrequisitos y límites de carga (máx 9).
    Devuelve: 
      El plan óptimo de cuatrimestres y estadísticas (nodos expandidos/generados).
    """
    frontera = [(0, estado_inicial, [])] # Cola de prioridad (costo, estado, ruta)
    visitados = set()
    
    while frontera:
        costo_actual, estado_actual, ruta = heapq.heappop(frontera)
        
        if is_goal(estado_actual, plan_estudios):
            return ruta, costo_actual
            
        if estado_actual in visitados:
            continue
            
        visitados.add(estado_actual)
        
        # Se generan transiciones combinando materias elegibles (1 a 9)
        for nueva_accion in generar_transiciones(estado_actual, plan_estudios):
            nuevo_estado = aplicar_transicion(estado_actual, nueva_accion)
            costo_paso = 1.0 + (len(nueva_accion) * 0.01)
            heapq.heappush(frontera, (costo_actual + costo_paso, nuevo_estado, ruta + [nueva_accion]))
            
    return None