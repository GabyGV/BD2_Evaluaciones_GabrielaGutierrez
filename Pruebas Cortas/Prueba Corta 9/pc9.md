# Prueba Corta 9

> Gabriela Gutiérrez Valverde - 2019024089

## ¿Por qué el uso de caches puede afectar el rendimiento del sistema de forma negativa?
En teoría la memoria caché mejora el rendimiento ya que guarda datos que son comunmente consultados y de esta manera no es necesario recurrir al disco, que suele ser más lento. En este caso en específico, nos dicen que hay mucha solicitud de datos **diferentes**, está es la razón por la que la memoria caché deja de ser tan eficiente y nos hace perder rendimiento, porque hay que realizar la consulta a la caché (que tiene datos recientes) pero muy probablemente el dato que se solicita no esté ahí, por lo que habría además que ir a hacer la consulta a disco y esto vuelve más lento el proceso. 

## ¿Cómo afecta el particionamiento y el sharding en el rendimiento de bases de datos SQL y NoSQL?
Puede afectar de forma positiva, sin embargo tiene una restricción negativa. De forma positiva, al aplicar el particionamiento en las bases SQL o el sharding en las bases NoSQL, se hace una división de los datos, esto puede mejorar la velocidad de las búsquedas, ya que en lugar de buscar la información en un solo grupo con todos los datos, se pueden hacer búsquedas sobre cada una de las particiones al mismo tiempo o en el caso del sharding se pueden hacer búsquedas específicas según se haya hecho su división. De forma negativa, si hay una consulta que necesite unir datos que se encuentran en varias particiones o shards, el tiempo de respuesta aumenta ya que es necesario hacer el reccorrido por todas las divisiones involucradas. 

# ¿Cómo afectan los exclusive locks el rendimiento de las bases de datos NoSQL?
Los exclusive locks permite que ocurra solamente una transacción a la vez, ya sea de lectura o de escritura, esto garantiza mucha consistencia pero si tenemos en cuenta que para poder utilizar un recurso debemos esperar hasta que la transacción anterior haga commit o rollback podemos ver cómo está bajando el rendimiento y los tiempos de respuesta suben. Ahora, las bases de Datos NoSQL están diseñadas para responder a consultas rápidas causando así que no sean muy consistentes.

# ¿Cómo afecta la selección de discos físicos el rendimiento de una base de datos SQL y NoSQL?
La mayor ventaja del disco físico es que no depende de una conexión de red, lo que puede ser más rápido y más estable. Y luego, el rendimiento va a depender también del tipo de disco físico que se tenga, incluso del tamaño de datos que podemos traer a la vez. Además, el rendimiento no solo se ve afectado por el tipo de disco físico sino que además lo afecta la forma en la que almacenemos los datos.