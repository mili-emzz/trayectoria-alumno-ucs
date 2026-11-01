# Resumen {#resumen .unnumbered}

Escribe aquí el resumen del reporte en español.

# Abstract {#abstract .unnumbered}

Write the summary of the report here..

# NOMBRE DEL PROYECTO

## Planteamiento del problema

Describir la problemática a resolver.

Es muy importante que esta sección sea explícita y detallada, es de las
que tiene más peso.

NOTA: todo objeto (figura, fórmula, tabla, citas, entre otros), debe
referenciarse en el texto del informe. Se penalizará si hay objetos no
referenciados desde el texto.

## PEAS

El marco PEAS se utiliza para describir y analizar agentes inteligentes
en Inteligencia Artificial. Éste define cómo un agente interactúa con su
entorno y ayuda a diseñar agentes que puedan alcanzar sus objetivos de
manera efectiva. Desglosa la interacción del agente con el entorno en
cuatro componentes clave:

### Medida de desempeño

Enunciar, explicar y justificar.

La métrica de rendimiento define cómo se evalúa el éxito de un agente.
Ayuda al agente a determinar si sus acciones están logrando el objetivo
deseado y lo guía para tomar mejores decisiones.

- Mide la eficacia de las acciones de un agente.

- Varía según la tarea y el entorno.

- Ayuda al agente a elegir las acciones que maximicen el éxito.

- Generalmente se define mediante objetivos o criterios de evaluación
  específicos.

Ejemplo: En un coche autónomo, la métrica de rendimiento puede incluir
la seguridad, el tiempo de viaje y la comodidad de los pasajeros.

### Entorno

Enunciar, explicar y justificar.

El entorno se refiere a todo lo que rodea a un agente y con lo que puede
interactuar o observar mientras realiza su tarea. Proporciona las
condiciones y la información que influyen en las decisiones y acciones
del agente.

- Representa el entorno en el que opera el agente.

- Puede cambiar con el tiempo a medida que el agente interactúa con él.

- Influye en cómo el agente percibe y responde a las situaciones.

- Comprender el entorno es fundamental para diseñar sistemas de IA
  eficaces.

Ejemplo: En el caso de un termostato inteligente, el entorno incluye la
temperatura ambiente, las condiciones climáticas, los sistemas de
calefacción o refrigeración y la presencia de personas.

#### Características del entorno

:::: center
::: {#TAB::DeliverableList}
  Característica                                       Justificación
  ---------------------------------------------------- ---------------
  Determinista o bien no determinista                  Justificar
  Monoagente o bien multiagente                        Justificar
  Completamente observable o parcialmente observable   Justificar
  Episódico o bien secuencial                          Justificar
  Discreto o continuo                                  Justificar
  Estático o bien dinámico                             Justificar
  Conocido o bien no conocido                          Justificar

  : Caracterización del entorno. Elegir la característica que aplica y
  justificar en términos del problema a resolver
:::
::::

### Actuadores

Enunciar, explicar y justificar.

Los Actuadores son los componentes mediante los cuales un agente realiza
acciones e interactúa con su entorno. Convierten las decisiones del
agente en acciones físicas o digitales.

- Ejecutar las acciones elegidas por el agente.

- Permitir que el agente interactúe con su entorno.

- Influir directamente en la capacidad del agente para lograr sus
  objetivos.

- Varían según el tipo de agente y la tarea.

Ejemplo: En un termostato inteligente, los actuadores incluyen el
sistema de calefacción, el sistema de refrigeración y los ventiladores
que regulan la temperatura ambiente.

### Sensores

Enunciar, explicar y justificar.

Los sensores son los componentes que recogen información del entorno y
se la proporcionan al agente. Esta información ayuda al agente a
comprender su entorno y a tomar las decisiones adecuadas.

- Recopilar datos del entorno.

- Ayuda al agente a percibir y comprender su entorno.

- Proporcionar la información necesaria para la toma de decisiones.

- La calidad de los sensores afecta al rendimiento del agente.

Ejemplo: En un termostato inteligente, los sensores pueden incluir
sensores de temperatura, sensores de humedad y sensores de movimiento
para monitorizar las condiciones ambientales.

## Especificación del problema de búsqueda

Especificar el problema de búsqueda, explicando

## Estado inicial

Ejemplificar el estado inicial, enunciar 2 o 3 ejemplos y explicarlos

## Meta

Ejemplificar meta, enunciar 2 o 3 ejemplos y explicarlos

## Espacio de estados

Especificar el tamaño del espacio de estados y colocar el proceso de
cálculo.

Ejemplificar los estados más importantes.

## Transiciones

Explicitar el orden en que se analizan las ramas.

Listar las transiciones posibles, usar una tabla

Si son demasiadas,ejemplificar las más importantes.

## Métricas de rendimiento

Enunciar, explicar y justificar las métricas de rendimiento
seleccionadas.

## Heurísticas

Enunciar, explicar y justificar las heurísticas seleccionadas.

# Implementación

En este capítulo deben documentar la implementación del algoritmo:

- Sólo se deben las correspondientes al método de búsqueda, dejar de
  lado las de visualización, se espera que en la implementación esté
  separado el método de búsqueda, se penalizará fuertemente si no hacen
  esa separación.

- Para cada método/función usar un bloque de código como el ejemplo, no
  se aceptará si usan capturas de pantalla para presentar código.

- Es imprescindible que cada función/método en un bloque de código deba
  llevar una explicación de qué parámetros recibe, qué hace y qué
  devuelve.

- Asegurar que desde la interfaz visual, se pueda cambiar el inicio o la
  meta, o el escenario.

Los bloques de código deberán presentarse de la siguiente manera:

``` {#LA.C1.A4.CODE::FuncTran .python language="Python" caption="Ejemplo de código insertado" label="LA.C1.A4.CODE::FuncTran"}
def incmatrix(genl1,genl2):
    m = len(genl1)
    n = len(genl2)
    M = None #to become the incidence matrix
    VT = np.zeros((n*m,1), int)  #dummy variable
    #compute the bitwise xor matrix
    M1 = bitxormatrix(genl1)
    M2 = np.triu(bitxormatrix(genl2),1) 
    for i in range(m-1):
        for j in range(i+1, m):
            [r,c] = np.where(M2 == M1[i,j])
            for k in range(len(r)):
                VT[(i)*n + r[k]] = 1;
                VT[(i)*n + c[k]] = 1;
                VT[(j)*n + r[k]] = 1;
                VT[(j)*n + c[k]] = 1;
                if M is None:
                    M = np.copy(VT)
                else:
                    M = np.concatenate((M, VT), 1)
                VT = np.zeros((n*m,1), int)
    return M
```

# Resultados

Presentar al menos tres ejemplos de la ejecución del algoritmo
resolviendo problemas no triviales.

Se busca evidenciar el funcionamiento en casos complejos.

Agregar una sección por cada ejemplo presentado.

## Caso 1

### Descripción

### Estado inicial y meta

Especificar el estado inicial y la meta a lograr.

Presentar la captura de pantalla sólo de la ventana de la interfaz
visual, donde se realiza la especificación

### Solución

Mostrar la solución.

Presentar la captura de pantalla sólo de la ventana de la interfaz
visual, donde se muestra la solución

### Ejecución

Mostrar la secuencia de imágenes de la ejecución de la solución.

Presentar la captura de pantalla sólo de la ventana de la interfaz
visual, donde se muestre paso a paso la ejecución de la tarea.

Pueden hacer un video que solo visualice la ventana de la interfaz
visual

### Comentarios

Reportar sus observaciones del caso analizado.

# Conclusiones y recomendaciones

## Conclusiones

¿Qué se aprendió una vez realizado el proyecto? ¿Qué cosas se
realizarían diferente si se tuviera que repetir el proyecto y por qué?
Una vez observado el resultado del proyecto, ¿qué nuevos proyectos se
podrían emprender?

## Recomendaciones

Recomendaciones sobre el desarrollo realizado.

Por ejemplo: módulos a refinar, tecnologías que deberán integrarse a
futuro.

# Anexos

Presentar cualquier información que consideren importante pero que no se
acomoda en las secciones antes mencionadas del informe.

Referenciar en el texto del informe los anexos, si los anexos no están
referenciados serán penalizados.
