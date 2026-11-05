# 🎓 Planificador de Trayectoria Académica (Ingeniería de Software)

Sistema inteligente basado en algoritmos de **búsqueda en espacio de estados** para la optimización de rutas académicas de estudiantes universitarios (especialmente en situación irregular), calculando el camino más corto hacia la graduación respetando seriaciones y cargas máximas.

---

## 📌 Descripción del Proyecto

En planes de estudio universitarios, cuando un estudiante reprueba o posterga materias, la malla curricular y las reglas de seriación vuelven complejo determinar qué materias cursar cada periodo para graduarse en el menor tiempo posible.

Este proyecto modela el mapa curricular como un problema de búsqueda de Inteligencia Artificial y utiliza el algoritmo **UCS (Uniform Cost Search / Búsqueda de Costo Uniforme)** para encontrar la trayectoria óptima que minimiza la cantidad de cuatrimestres restantes, cumpliendo con:
- **Prerrequisitos / Seriación estricta** de asignaturas.
- **Límites de carga académica** por periodo (mínimo y máximo de materias).
- **Materias especiales** con restricciones (ej. estancias profesionales).

---

## 🚀 Características Principales

- 🧠 **Algoritmo de IA:** Implementación de Búsqueda de Costo Uniforme (UCS) que garantiza la ruta óptima en número de periodos y costo acumulado.
- 💻 **Interfaz Gráfica (GUI):** Desarrollada en Tkinter, amigable e intuitiva para marcar materias cursadas, seleccionar el cuatrimestre de avance y visualizar el plan sugerido periodo a periodo.
- ⚙️ **Modos Rápidos:** Botón para cargar automáticamente el perfil de alumno regular según el cuatrimestre seleccionado.
- 📊 **Métricas y Resultados:** Muestra la secuencia detallada de inscripción, cuatrimestres necesarios y métricas del algoritmo (nodos explorados, tiempo de cómputo).

---

## 📁 Estructura del Repositorio

```text
├── main.py              # Punto de entrada de la aplicación
├── src/
│   ├── curriculum.py    # Definición de materias, prerrequisitos y reglas de la carrera
│   ├── solver.py        # Modelo del espacio de estados y algoritmo de búsqueda (UCS)
│   └── ui.py            # Interfaz gráfica de usuario con Tkinter
├── docs/                # Documentación técnica, manual de usuario y casos de prueba
└── README.md            # Este archivo
```

---

## 🛠️ Requisitos e Instalación

### Requisitos Previos
- **Python 3.10 o superior**
- Biblioteca `tkinter` (incluida por defecto en la mayoría de instalaciones estándar de Python en Windows/Mac).

No requiere dependencias externas pesadas (`pip install` adicional no necesario).

---

## 💻 Instrucciones de Uso

1. **Clonar o descargar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd proyecto
   ```

2. **Ejecutar la aplicación:**
   ```bash
   python main.py
   ```

3. **Dentro de la aplicación:**
   - Selecciona el **cuatrimestre actual**.
   - Marca las materias que ya tienes **aprobadas** (o haz clic en *Regular* para marcarlas según tu cuatrimestre).
   - Presiona **Resolver**.
   - Consulta el plan cuatrimestre por cuatrimestre generado en el panel derecho.

Para más detalles paso a paso, consulta el [Manual de Uso](docs/manual_de_uso.md).

---

## 📚 Documentación Adicional

- [Documentación Técnica y Teórica](docs/documentaci_n_del_proyecto.md): Formulación matemática del espacio de estados, operadores y análisis del algoritmo.
- [Manual de Uso](docs/manual_de_uso.md): Guía visual detallada con ejemplos prácticos.
