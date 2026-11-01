# 🎓 Manual de Uso — Planificador de Trayectoria Académica IS

> [!NOTE]
> Esta app usa el algoritmo **UCS (Búsqueda de Costo Uniforme)** para encontrar el plan de materias **más corto** que te lleva de tu situación actual hasta graduarte (Estancia II).

---

## ¿Cómo se ve la app?

```
┌──────────────────────────────────────────────────────────────────────┐
│  🎓 Planificador de Trayectoria Académica — Ingeniería en Software   │
├──────────────────────────┬───────────────────────────────────────────┤
│  ⚙ Configuración         │  📊 Plan de Recuperación Óptimo           │
│                          │                                           │
│  Cuatrimestre actual: [4]│  (aquí aparece el resultado)              │
│                          │                                           │
│  [✅ Resolver] [🔄 Lim]  │                                           │
│  [👤 Regular]            │                                           │
│                          │                                           │
│  📋 Materias aprobadas:  │                                           │
│  ── Cuatrimestre 1 ──    │                                           │
│  ☑ Algoritmos            │                                           │
│  ☐ Álgebra Lineal        │                                           │
│  ...                     │                                           │
├──────────────────────────┴───────────────────────────────────────────┤
│  Barra de estado: "Listo. Configura el alumno y presiona Resolver."  │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Paso a paso para usarla

### 1️⃣ Configura tu cuatrimestre actual

El **spinbox** (la cajita con flechitas ▲▼) dice `Cuatrimestre actual`.

- Haz clic en las flechitas **▲** o **▼** para subir/bajar el número.
- También puedes **hacer clic en el número** y escribir directamente (del 1 al 10).
- **¿Qué poner aquí?** El cuatrimestre en el que estás **ahorita**. Si ya terminaste el 3er cuatrimestre y vas a empezar el 4to, pon `4`.

> [!IMPORTANT]
> Este número le dice al algoritmo desde qué punto eres capaz de cursar materias. Si lo pones muy bajo, el algoritmo asumirá que no puedes tomar materias avanzadas todavía.

---

### 2️⃣ Marca las materias que ya aprobaste

En la lista de la izquierda aparecen **todas las materias de la carrera**, agrupadas por cuatrimestre (en amarillo).

- ✅ **Marca** (haz clic en el checkbox) cada materia que **ya cursaste y aprobaste**.
- ❌ Deja **sin marcar** las materias que aún te faltan o que reprobaste.
- Puedes hacer **scroll** con la rueda del mouse dentro de esa lista.

> [!TIP]
> Si eres alumno regular (no reprobaste nada), **no** tengas que marcar todo a mano. Usa el botón 👤 Regular (ver abajo).

---

### 3️⃣ Usa los botones

| Botón | ¿Para qué sirve? |
|---|---|
| **✅ Resolver** | Corre el algoritmo UCS y te muestra el plan óptimo de cuatrimestres para graduarte. ¡Este es el botón principal! |
| **🔄 Limpiar** | Desmarca **todas** las materias y borra el resultado. Útil para empezar desde cero. |
| **👤 Regular** | Marca automáticamente como aprobadas todas las materias de los cuatrimestres **anteriores** al que configuraste. |

#### ¿Cómo usar 👤 Regular?

1. Pon el cuatrimestre actual (p.ej., `5`).
2. Presiona **👤 Regular**.
3. La app marcará automáticamente todas las materias de los cuatrimestres 1, 2, 3 y 4.
4. Ya solo tendrás que marcar manualmente si reprobaste alguna (desmárcala) o si adelantaste alguna extra (márcala).

---

### 4️⃣ Presiona ✅ Resolver y lee el resultado

El panel derecho mostrará tu plan cuatrimestre a cuatrimestre. Ejemplo:

```
══════════════════════════════════════════════════════════════
   PLAN DE TRAYECTORIA ÓPTIMO — INTELIGENCIA ARTIFICIAL
══════════════════════════════════════════════════════════════
  Cuatrimestre de inicio   : 5
  Costo total acumulado    : 6.06
  Periodos hasta graduación: 6

[CUATRIMESTRE 5]  (Carga: 3 materias)
   • Calidad del Software
   • Compiladores e Intérpretes
   • Probabilidad y Estadística

[CUATRIMESTRE 6]  (Carga: 4 materias)
   • ...

🎉 ¡ESTADO META ALCANZADO — GRADUACIÓN! 🎉
```

**¿Qué significa cada dato?**

| Dato | Significado |
|---|---|
| **Cuatrimestre de inicio** | El cuatrimestre que tú configuraste |
| **Costo total acumulado** | Número interno del algoritmo (cuatrimestres + penalización por carga) |
| **Periodos hasta graduación** | **Cuántos cuatrimestres más** necesitas para terminar la carrera |
| **[CUATRIMESTRE N]** | Las materias que el algoritmo recomienda tomar en ese periodo |
| **Nodos expandidos/generados** | Estadísticas del algoritmo UCS (para la parte de IA del proyecto) |

---

## Casos de uso típicos

### 🟢 Caso 1: Alumno sin irregularidades

1. Pon tu cuatrimestre actual (p.ej., `4`).
2. Presiona **👤 Regular** → se marcan cuatrimestres 1, 2 y 3.
3. Presiona **✅ Resolver**.
4. Verás el plan de los cuatrimestres 4 en adelante.

### 🟡 Caso 2: Reprobé una materia

1. Pon tu cuatrimestre actual.
2. Presiona **👤 Regular**.
3. Busca la materia que reprobaste en la lista y **desmárcala** (clic para quitar el ✓).
4. Presiona **✅ Resolver**.
5. El algoritmo calculará un plan que incluya esa materia pendiente.

### 🔴 Caso 3: Entrar desde cero (cuatrimestre 1)

1. Pon `1` en el cuatrimestre.
2. **No marques nada** (o presiona **🔄 Limpiar** para asegurarte).
3. Presiona **✅ Resolver**.
4. Verás el plan completo de toda la carrera.

---

## Detalles del algoritmo (para el reporte)

El algoritmo es **UCS (Uniform-Cost Search)**:

- **Estado:** conjunto de materias aprobadas + cuatrimestre vigente.
- **Acción:** elegir un grupo de materias elegibles para tomar en un cuatrimestre.
- **Costo de un paso:** `1.0 + 0.01 × número_de_materias`
  - El `1.0` hace que el algoritmo minimice **el número de cuatrimestres** (objetivo principal).
  - El `0.01 × n` es un desempate: ante igual número de cuatrimestres, prefiere la **carga más ligera**.
- **Meta:** haber aprobado **el 100% de las materias del plan de estudios** (no dejar materias huérfanas sin cursar).
- **Carga máxima:** 9 materias por cuatrimestre.

> [!NOTE]
> Una materia es elegible si: (1) no está aprobada, (2) todos sus prerrequisitos sí están aprobados, y (3) su nivel de cuatrimestre ≤ cuatrimestre actual del alumno.

---

## Errores comunes

| Error / situación | Qué hacer |
|---|---|
| Sale "❌ No se encontró solución" | Verifica que las materias marcadas sean coherentes. Por ejemplo, no marques Programación Web sin haber marcado Programación Visual. |
| El resultado tarda mucho | Es normal si tienes pocas materias aprobadas; el UCS explora más estados. Espera un momento. |
| Quiero comparar dos escenarios | Usa **🔄 Limpiar**, reconfigura y vuelve a resolver. |
