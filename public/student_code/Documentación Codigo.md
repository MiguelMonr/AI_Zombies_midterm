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

A partir de esta policy ya se nos es permitido tomar en cuenta la información que se ha acumulado durante esta época de crisis, eso incluye información de las simulaciones pasadas. Es decir, ya tenemos más datos a nuestra disposición.

Para esta policy buscamos una relación entre los proxys que se nos fueron otorgados durante la policy 2, es así que se establece una penalización a la arista en donde se encuentren ciertos “datos” (los los escombros, la densidad poblacional, etc.), dándole un mayor peso y así evitando esa ruta completamente. Es así que para llegar al nodo deseado usamos Djikstra, pero este corre bajo las penalizaciones dadas a los nodos, considerando sus nuevos pesos y calculando una ruta segura y lo más rápida posible. 

Además, considera los recursos que se tienen a disposición, es decir, que si no se disponen de los recursos suficientes y considerando las relaciones dadas anteriormente, es capaz de elegir otra ruta que se adapte a las necesidades. Adicionalmente, estos recursos son seleccionados en relación con la cantidad de escombros o población en la ruta



# Ventajas: El actualizar los pesos de las aristas es aprovechar toda la información dada de manera previa, penalizando rutas peligrosas y ayudando a la flexibilidad de asignación de recursos, además, considera rutas alternativas siempre que esa asignación no sea adecuada para la ruta considerada inicialmente.
# Desventajas: Depende de la calidad de datos recopilados anteriormente, no garantiza una ruta óptima al usar heurísticas para seleccionar rutas alternativas

Análisis de la política desde la perspectiva de probabilidad de Jaynes y su robot.

Uso de toda la información, la inicial usando el layout de la ciudad, la que se relaciona con la proxy, y, finalmente, la información recopilada de todas las misiones previas
Enfoque estadístico y basado en datos

---

# Política 4: Simulación de Entrenamiento

Esta vez se usa BFS para conocer los caminos a los nodos de extracción, sin embargo, también introduce un umbral que, en caso de ser excedido, fuerza a buscar una ruta alternativa, descartando las aristas con un umbral demasiado alto. 
Asimismo, se calcula la cantidad de escombros, población y radiación en esas rutas para seleccionar de manera proporcional los recursos disponibles

# Ventajas: 
Permite explorar rutas con riesgo moderado, y si no puede encontrar una con ese nivel busca uno con un umbral intermedio, buscando siempre la mejor ruta posible. Los umbrales facilitan la adaptación a nuevos escenarios.
# Desventajas: 
También depende de la calidad de los datos recopilados con anterioridad.


Análisis de la política desde la perspectiva de probabilidad de Jaynes y su robot.
Usa umbrales para decidir si conviene o no tomar una ruta, es decir, utiliza números reales y valores numéricos para tomar decisiones
Es consistente, ya que sigue un sistema que le asigna valores a los umbrales de manera lógica, usando siempre las mismas reglas

