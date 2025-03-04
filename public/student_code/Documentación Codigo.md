# Política 1: Los primeros días

Ya que se cuenta con la información de la estructura de la Ciudad, se implementa **A*** para plantear el posible camino óptimo cuyo resultado sea una extracción. En caso de que el camino no exista, se dan **0 recursos**, con el fin de empezar a acumular información.

### Desventajas:
- No se posee la información, por lo que posiblemente ese camino tenga mayor riesgo.
- **A*** no toma la administración de recursos, lo cual es sumamente difícil en este contexto.

### Ventajas:
- Camino más corto.
- Balance entre **BFS** y **Dijkstra**.

Al no tener información, **asignamos recursos aleatorios**.

### Análisis de la política desde la perspectiva de probabilidad de Jaynes y su robot:
- **A*** es un método lógico consistente, por lo que cumple la desiderata de consistencia.
- Ya que la asignación de recursos es aleatoria, **no se cumple con la segunda desiderata**.
- Se usa toda la información disponible, pero **no es óptimo**, porque el resultado depende de cuestiones que desconocemos.

---

# Política 2: Estableciendo la Red de Monitoreo

> **OJO**: Implementación, compilación y covarianza.

Dado el **proxy de actividad sísmica**, se implementará que:
- Si la actividad sísmica es de **0.75** y se tienen **menos de 2 explosivos**, se escoge el siguiente camino más corto, pero **que no pase por ahí**.
- Si no existe dicho camino, **se aumentará el número de explosivos** que llevará el grupo.

Dado el **proxy de radiación**:
- Si el valor es **1**, se evita el camino directamente.
- Si el valor está entre **0.4 y 0.75**, y solo se tiene **un traje**, también se evita.
- Si hay trajes para todos, **se toma el camino**.

Dado el **proxy de densidad de población**:
- Si es **1** y se tienen **menos de 5 balas**, se evita el lugar.
- De lo contrario, se toma ese camino.
- Si no existe otro camino y se pueden llevar más balas, **se triplica la cantidad de balas** (de ser posible).

Dado el **proxy de llamadas de emergencia**:
- Si es **mayor a 0.8**, **se evitará el camino**.
- De lo contrario, se toma.

Dado el **proxy de la actividad térmica**:
- Si el patrón térmico es constantemente consistente y el número de balas es menor a **3**, **se evita el lugar**.
- De lo contrario, **se toma el camino**.

El **proxy de fuerza de señal** no tiene relevancia por ahora, dado que al implementar **A***, es irrelevante para marcar un camino óptimo.

Si las lecturas del **proxy de integridad estructural** son **bajas**, **se evitará a toda costa pasar por ahí**, a menos de que **sea el único camino**.

Todo lo anterior tomando en cuenta que siempre **se buscará el siguiente camino más corto**.

### Desventajas:
- Las reglas están definidas de forma **fija** y no adaptativa.
- Algunas son arbitrarias y no sirven para todos los casos.

### Ventajas:
- Se empieza a tomar en cuenta la información de los sensores, por lo que **la probabilidad de sobrevivir aumenta**.

Al no tener información, **asignamos recursos aleatorios**.

### Análisis de la política desde la perspectiva de probabilidad de Jaynes y su robot:
- **A*** es un método lógico consistente, pero al incluir los **proxys**, ya no se sigue siempre lo **óptimo** en términos de camino más corto.
- Ahora el enfoque está en usar los **proxys** a fin de **garantizar éxito**.
- Al tener ya **proxys disponibles**, tenemos mayor cantidad de información para implementar en nuestro algoritmo.
- Sin embargo, aún no tenemos disponible la información de **simulaciones previas**.

---

# Política 3: Aprendiendo de la Experiencia

- **Mayor relación con valor absoluto**.
- **Gradiente de peligro creado**.

### Para P1: Menor gradiente de peligro. ¿Qué pasó?
- Se suman los valores y aquellos negativos **se suman al revés**.
- **Se asignan los recursos con esa distribución**.

Tomando en cuenta el **success rate** de las misiones previas:
- Se identifican las condiciones de las misiones con el **success rate** más alto.
- Usando **regresión lineal**, se estudia el número de recursos utilizados y su cercanía con el nodo al que se quería llegar, para identificar **qué tan relevantes son los recursos**.
- Se analiza cada uno de los recursos por separado, así como en conjunto.
- También se analizará el resultado de seguir los **proxys** cuando los recursos se suponían suficientes para sobrellevar la situación y se comparará con el resultado de evitar dicho nodo.

### Desventajas:
- Se puede estar usando un **dato estadístico inadecuado**.
- Puede ser **demasiado rígido** para capturar relaciones complejas entre variables.
- Podría tomar **patrones irrelevantes** y no tendencias generales.

### Ventajas:
- Proporciona un **método cuantitativo y cualitativo** para tomar decisiones.
- Ayuda a **entender patrones** y factores que pueden conducir al éxito.
- Evita el **desprecio de productos**.

### Análisis de la política desde la perspectiva de probabilidad de Jaynes y su robot:
- **Uso de toda la información**:
  - La inicial, usando el **layout** de la ciudad.
  - La relacionada con los **proxys**.
  - La información recopilada de **todas las misiones previas**.
- Enfoque **estadístico y basado en datos**.

---

# Política 4: Simulación de Entrenamiento

En este caso **no tenemos moral ni consecuencias**, sólo buscamos **optimizar y aprender**. 

Es por ello que la mejor manera de optimizar es **mandar a la mayor cantidad de personas, sin recursos**, para aprender cómo funciona este nuevo mundo postapocalíptico y saber qué esperar de cada nodo. 

Esto nos ayudará a saber **cómo y cuántos recursos llevar** dependiendo de este nuevo conocimiento que surgió gracias al **sacrificio de miles de ciudadanos inocentes** (**RIP**).
