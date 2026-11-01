# Propuesta Técnica: Optimización de Trayectorias Académicas para Alumnos Irregulares

**Materia:** Fundamentos de Inteligencia Artificial

**Tema:** Algoritmos de Búsqueda no Informada / Búsqueda en Espacio de Estados

**Fecha:** Noviembre de 2026

## 1. Definición del Escenario y Problema

### 1.1 Contexto

En las instituciones de educación superior, un alumno adquiere el estatus de **irregular** cuando reprueba o deja de cursar ciertas asignaturas dentro de la secuencia sugerida por el mapa curricular. La gestión académica requiere diseñar planes de recuperación que permitan al alumno regularizar su situación e incorporarse a la graduación en el **menor tiempo posible (menor número de cuatrimestres/periodos)** sin someterlo a cargas académicas excesivas o inviables.

### 1.2 Definición Formal del Problema de IA

El problema consiste en modelar el mapa de seriación académica como un **grafo de decisiones secuenciales** y aplicar algoritmos de búsqueda no informada para encontrar una trayectoria óptima $T^*$, la cual especifica qué subconjunto de materias debe inscribir el estudiante en cada cuatrimestre futuro para alcanzar la graduación (aprobar el 100% de las asignaturas) satisfaciendo todas las restricciones operativas e institucionales.

## 2. Definición Formal del Agente y Espacio de Estados

### 2.1 Representación del Estado ($S$)

Un estado en el espacio de búsqueda no representa una materia individual, sino la **fotografía completa del expediente y avance académico** del estudiante en un periodo dado.

Formalmente, un estado $S_i$ se define como la tupla:

$$
S_i = (A_i, T_i)
$$

Donde:

* $A_i \subseteq \mathcal{U}$: Es el conjunto de asignaturas aprobadas por el estudiante hasta el periodo $i$, siendo $\mathcal{U}$ el universo total de materias del plan de estudios.

* $T_i \in \mathbb{N}$: Es el cuatrimestre/periodo lectivo actual en el que se encuentra posicionado el estudiante ($T_i = 1, 2, 3, \dots, N$).

### 2.2 Estado Inicial ($S_0$)

$$
S_0 = (A_{\text{inicial}}, T_{\text{reincorporación}})
$$


Donde $A_{\text{inicial}}$ es el conjunto de asignaturas que el alumno ya tiene acreditadas previamente, y $T_{\text{reincorporación}}$ es el periodo escolar en el que vuelve a cursar materias.

### 2.3 Condición Meta (Goal Test)

El algoritmo evalúa si un estado $S_i = (A_i, T_i)$ es un estado meta mediante la función:

$$
\text{IsGoal}(S_i) = \begin{cases} \text{True} & \text{si } A_i = \mathcal{U} \\ \text{False} & \text{en otro caso} \end{cases}
$$

Es decir, el objetivo se alcanza cuando el conjunto de materias aprobadas equivale a la totalidad del plan de estudios.

## 3. Transiciones, Acciones y Reglas de Validez

### 3.1 Conjunto de Materias Cursables ($M_{\text{cursables}}$)

Dado un estado $S_i = (A_i, T_i)$, una asignatura $m \in \mathcal{U} \setminus A_i$ es elegible para ser cursada si cumple **ambas** condiciones:

1. **Cumplimiento de Prerrequisitos:** $\text{Pre}(m) \subseteq A_i$, donde $\text{Pre}(m)$ son las materias seriadas directamente con $m$.

2. **Restricción de Nivel/Cuatrimestre:** $\text{Nivel}(m) \le T_i$. Un estudiante no puede cursar materias de un nivel superior a su cuatrimestre actual, pero sí puede cursar materias pendientes de niveles anteriores.

### 3.2 Generación de Transiciones (Acciones)

Una acción o transición $a$ consiste en seleccionar un subconjunto $k$ de $M_{\text{cursables}}$ para ser inscritas en el periodo $T_i$:

$$
a = \{m_1, m_2, \dots, m_k\} \subseteq M_{\text{cursables}}
$$

**Restricciones de la Transición:**

* **Carga Máxima por Periodo:** $1 \le \vert{}a\vert{} \le 9$ (máximo 9 asignaturas por cuatrimestre).

* **Límite de Convalidaciones/Cursos Especiales:** Máximo 2 asignaturas bajo modalidad de convalidación o examen especial por periodo.

### 3.3 Función de Transición de Estado

Al aplicar la acción $a$ sobre el estado $S_i = (A_i, T_i)$, se transiciona al nuevo estado $S_{i+1}$:

$$
\text{Result}(S_i, a) = (A_i \cup a, T_i + 1)
$$

## 4. Propiedades del Entorno de IA

El entorno de resolución del problema se clasifica bajo las siguientes propiedades formales:

| Propiedad | Clasificación | Justificación Téorica | 
| ----- | ----- | ----- | 
| **Observabilidad** | Completely Observable | Se conoce el 100% del mapa curricular, seriación y el expediente del alumno. | 
| **Determinismo** | Determinista | Como planificación estática, se asume que si el alumno inscribe una materia la aprueba al final del periodo. | 
| **Secuencialidad** | Secuencial | La decisión de inscribir materias en $T_i$ condiciona las materias desbloqueadas para $T_{i+1}$. | 
| **Dinamismo** | Estático | Las reglas del plan de estudios, las seriaciones y la oferta no cambian mientras la IA calcula la ruta. | 
| **Continuidad** | Discreto | El espacio de estados, las materias y los cuatrimestres son finitos y contables. | 
| **Agentes** | Monoagente | Se modela la trayectoria individual de un único estudiante de forma aislada. | 

## 5. Selección y Justificación del Algoritmo de Búsqueda

### 5.1 Comparativa de Algoritmos Evaluados

1. **Depth-First Search (DFS):**

   * *Descarte:* No es adecuado. DFS profundiza por una rama hasta el final antes de retroceder, lo que podría sugerirle al alumno un camino largo e ineficiente (ej. llevar de 2 en 2 materias y tardar 15 cuatrimestres en graduarse). No garantiza optimidad.

2. **Breadth-First Search (BFS):**

   * *Viabilidad:* Válido. Como la profundidad en el árbol de búsqueda corresponde directamente a **cuatrimestres transcurridos**, BFS garantiza encontrar la solución con el menor número de periodos escolares.

   * *Limitación:* BFS trata todas las combinaciones de carga por igual. Elegirá indistintamente una opción de 9 materias sobre una de 5 materias si ambas llegan al mismo cuatrimestre.

3. **Uniform-Cost Search (UCS) / Búsqueda de Costo Uniforme:**

   * **Algoritmo Seleccionado.** UCS expande el nodo con el menor costo acumulado $g(n)$. Permite diseñar una función de costo multicriterio.

### 5.2 Diseño de la Función de Costo para UCS

Para satisfacer el objetivo principal (**minimizar tiempo**) y el objetivo secundario (**no sobrecargar al estudiante**), definimos el costo $c(S_i, a, S_{i+1})$ de realizar una transición $a$:

$$
c(S_i, a, S_{i+1}) = 1.0 + (\vert{}a\vert{} \times \epsilon)
$$

Donde:

* $1.0$: Es el costo base por cada cuatrimestre transcurrido.

* $\vert{}a\vert{}$: Es el número de asignaturas inscritas en esa transición ($1 \le \vert{}a\vert{} \le 9$).

* $\epsilon$: Es un penalizador marginal muy pequeño (ej. $\epsilon = 0.01$).

**Efecto Teórico:**

* Al ser el costo del cuatrimestre ($1.0$) infinitamente superior a la penalización por materia ($0.01 \cdot 9 = 0.09$), el algoritmo **priorizará siempre graduar al estudiante en el menor número de cuatrimestres**.

* Si existen dos trayectorias que gradúan al alumno en la misma cantidad de cuatrimestres (ej. 3 periodos), UCS elegirá la ruta con **menor costo acumulado total**, seleccionando automáticamente la opción con la carga académica más ligera y equilibrada.

## 6. Diagrama Conceptual del Árbol de Búsqueda

```
                                [ ESTADO INICIAL ]
                        S0 = ({Aprobadas_Previas}, T=4)
                                 g(n) = 0.0
                                     │
               ┌─────────────────────┴─────────────────────┐
               │                                           │
     Acción A: {BD, PE} (2 materias)             Acción B: {BD} (1 materia)
     Costo paso = 1.0 + (2 * 0.01) = 1.02        Costo paso = 1.0 + (1 * 0.01) = 1.01
               │                                           │
               ▼                                           ▼
  [ ESTADO INTERMEDIO S1 ]                    [ ESTADO INTERMEDIO S2 ]
 S1 = ({Aprobadas, BD, PE}, T=5)            S2 = ({Aprobadas, BD}, T=5)
       g(n) = 1.02                                  g(n) = 1.01
               │                                           │
   (¡Se desbloquea MD!)                        (Aún NO se desbloquea MD)
               │                                           │
     Acción A1: {PW, MD}                        Acción B1: {PE, PW}
     Costo paso = 1.02                          Costo paso = 1.02
               │                                           │
               ▼                                           ▼
     [ ESTADO META S_META1 ]                    [ ESTADO INTERMEDIO S3 ]
   ({Todas Aprobadas}, T=6)                    ({Aprobadas, BD, PE, PW}, T=6)
       g(n) = 2.04                                  g(n) = 2.03
   ★ RUTA ÓPTIMA SELECCIONADA ★                             │
                                                Acción B2: {MD}
                                                Costo paso = 1.01
                                                           │
                                                           ▼
                                                [ ESTADO META S_META2 ]
                                              ({Todas Aprobadas}, T=7)
                                                    g(n) = 3.04

```

## 7. Conclusión del Diseño

El modelado del problema bajo el enfoque de **Búsqueda en Espacio de Estados con UCS** garantiza formalmente:

1. Respetar de forma estricta las seriaciones y restricciones del plan de estudios.

2. Encontrar la ruta más corta en cuanto a tiempo (cuatrimestres).

3. Resolver empates mediante la selección de trayectorias con menor saturación académica para el estudiante.