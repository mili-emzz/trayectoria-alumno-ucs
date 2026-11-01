# Plan de Desarrollo, Métricas de Evaluación y Flujo de Implementación

## 1\. Flujo de Implementación (Fases de Desarrollo)

El desarrollo del proyecto se divide en 4 fases principales para garantizar un diseño modular y fácil de depurar:

```
 ┌─────────────────────────────────────────────────────────┐
 │ FASE 1: Modelado de Datos y Estructura del Mapa         │
 │ - Definir catálogo de asignaturas con sus cuatrimestres │
 │ - Construir el grafo de seriación (prerrequisitos)      │
 └────────────────────────────┬────────────────────────────┘
                              │
                              ▼
 ┌─────────────────────────────────────────────────────────┐
 │ FASE 2: Motor de Transiciones y Reglas de Negocio       │
 │ - Algoritmo para obtener materias elegibles             │
 │ - Generador de combinaciones de carga (1 a 9 materias)  │
 │ - Filtrado de restricciones (máx. 2 convalidaciones)   │
 └────────────────────────────┬────────────────────────────┘
                              │
                              ▼
 ┌─────────────────────────────────────────────────────────┐
 │ FASE 3: Algoritmo de Búsqueda (UCS)                     │
 │ - Implementación de la cola de prioridad (`heapq`)     │
 │ - Definición del cálculo del costo acumulado $g(n)$     │
 │ - Control de nodos visitados para evitar ciclos        │
 └────────────────────────────┬────────────────────────────┘
                              │
                              ▼
 ┌─────────────────────────────────────────────────────────┐
 │ FASE 4: Pruebas, Métricas e Interfaz de Salida          │
 │ - Creación de casos de prueba (alumnos irregulares)     │
 │ - Medición de desempeño (tiempo, memoria, nodos)        │
 │ - Formateador del plan de estudios resultante           │
 └─────────────────────────────────────────────────────────┘
```

---

## 2\. Métricas para Saber que el Proyecto está Bien Realizado (Criterios de Aprobación)

Para considerar el proyecto un éxito académico y funcional, la solución debe cumplir con dos categorías de métricas: **Correctitud de IA/Dominio** y **Desempeño del Algoritmo**.

### A. Métricas de Correctitud y Dominio (Validez Educativa)

1. **Garantía de Secuencia Causal (No Violación de Prerrequisitos):**

   * *Métrica:* $0\%$ de violaciones de seriación en el plan generado.
   * Ninguna asignatura $m$ se inscribe en el periodo $T$ sin que sus prerrequisitos $\text{Pre}(m)$ hayan sido aprobados en un periodo $T'<T$.  
2. **Cumplimiento de Restricciones Operativas:**

   * Carga académica por periodo: $1 \le \text{materias} \le 9$.  
   * Convalidaciones por periodo: $\leq 2$.  
   * Restricción de cuatrimestre superior: Ninguna materia de nivel $> T_{\text{actual}}$ inscrita.  
3. **Alcanzabilidad del Estado Meta (Completitud):**

   * El algoritmo debe garantizar que el estado final contenga el $100\%$ del plan de estudios de la carrera.

### B. Métricas de Desempeño Técnico y Optimización (Validez de IA)

1. **Optimidad en Tiempo (Menor Número de Cuatrimestres):**

   * El número de cuatrimestres de la ruta seleccionada $T_{\text{graduación}}$ debe ser **mínimo estricto**. No debe existir ningún otro camino válido en el grafo con menor número de periodos.  
2. **Carga Académica Distribuida / Minimización de Sobrecarga:**

   * Entre dos rutas con igual número de cuatrimestres, la métrica elegirá la de menor costo acumulado $g(n)$, evitando saturar al estudiante con 9 materias si con 5 o 6 obtiene exactamente el mismo tiempo de egreso.  
3. **Eficiencia en el Espacio de Búsqueda:**

   * **Nodos Expandidos vs. Nodos Generados:** Medir la capacidad del algoritmo para recortar ramas inválidas antes de meterlas a la cola de prioridad.  
   * **Tiempo de Ejecución:** El algoritmo debe devolver la trayectoria en menos de 5 segundos para un alumno con hasta 10 materias reprobadas/pendientes.

---

## 3\. Matriz de Pruebas (Casos de Validación)

Para demostrar la efectividad del proyecto en tu presentación o reporte, se deben probar 3 escenarios tipo:

| Caso de Prueba | Descripción del Alumno | Resultado Esperado |
| :---- | :---- | :---- |
| **Caso 1: Alumno Regular** | No debe materias, está en cuatrimestre $N$. | Retorna la trayectoria estándar sugerida por la carrera. |
| **Caso 2: Cuello de Botella** | Reprobó materias que abren cadenas largas de seriación (ej. Programación Básica $\rightarrow$ POO $\rightarrow$ Web). | El algoritmo identifica la rama crítica y le da máxima prioridad para inscribirla lo antes posible. |
| **Caso 3: Carga Dispersa** | Reprobó muchas materias aisladas sin seriación fuerte (ej. 7 materias de diferentes áreas). | El algoritmo agrupa eficientemente hasta 9 materias por periodo para "emparejarlo" al cuatrimestre correcto rápido. |

---

## 4\. Estructura Sugerida de Salida del Programa

El programa debe imprimir un reporte claro para el alumno y docente, similar a este:

```
======================================================================
         PLAN DE RECUPERACIÓN ÓPTIMO - INTELIGENCIA ARTIFICIAL
======================================================================
Estado Inicial: Alumno en Cuatrimestre 4 (Materias pendientes: 6)
Costo Total Acumulado g(n): 3.14
Cuatrimestres Totales para Graduación: 3 periodos

[CUATRIMESTRE 4] (Carga: 5 materias | Convalidaciones: 1)
 - Base de Datos (Clave: BD01)
 - Probabilidad y Estadística (Clave: PE01)
 - Expresión Oral y Escrita II (Clave: EO02)
 ...

[CUATRIMESTRE 5] (Carga: 4 materias)
 - Minería de Datos (Desbloqueada por BD01 + PE01)
 - Programación Web (Clave: PW01)
 ...

[CUATRIMESTRE 6] -- ESTADO META ALCANZADO 🎉
 - Proyecto Integrador / Estadía
======================================================================
Estadísticas del Algoritmo UCS:
 - Nodos expandidos: 142
 - Nodos en memoria: 480
 - Tiempo de cómputo: 0.12 segundos
======================================================================
```

&nbsp;