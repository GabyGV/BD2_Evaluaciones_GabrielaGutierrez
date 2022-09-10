# Prueba Corta 2

> Gabriela Gutiérrez Valverde - 2019024089

## Explique el concepto de shard, replica y partition.
1. **Shard:** una partición horizontal de una base de datos. Es decir, se crear nuevas tablas con los mismos atributos pero se distribuyen los datos. Ayuda a acelerar el tiempo de respuesta y al crecimiento horizontal de la base de datos.
2. **Replica:** es una nueva instancia de la base de datos generalmente en otra ubicación para poder copiar, distribuir y luego sincronizar entre las bases para poder mantener la consistencia.
3. **Partition:** es cuando una tabla grande se divide en tablas más pequeñas, permite que las consultas sean más rápidas ya que hay menos datos en las tablas resultantes.

## Explique la diferencia entre Strong Consistency Eventual Consistency.
Strong Consistency significa que debe haber muy alta consistencia en los datos todo el tiempo, significa que los datos deben estar bloqueados al momento de realizar una actualización o una réplica para asegurar que no existan otros procesos modificando los datos. Mientras que Eventual Consistency, significa que permite que la base esté disponible todo el tiempo pero podría dar como resultado de una consulta datos que no estén actualizados.

## ¿En que consiste warm replicas y hot replicas?
- **Warm replicas:** significa que la primera réplica se almacena en disco y las demás se almacenan en archivo. Ocupa más Disco, pero menos CPU y RAM.
- **Hot replicas:** significa que todas las réplicas se almacenan en disco. Ocupa más CPU, RAM y Disco.

| TIPO | RAM | DISCO |
| ------ | ------ | ------ |
| WARM | 1GB | 30GB |
| HOT | 1GB | 60GB |


## ¿En que consiste consiste switch over y fail over?
- **Switch over:** es un cambio entre la base de datos de datos principal y una de las que se encuentra en espera, garantiza que no haya pérdida de datos. La BD en espera toma el papel de principal y la que antes era la principal toma el papel en espera, es un proceso controlado, normalmente planificado.
- **Fail over:** es cuando la base de datos principal falla y entonces una de las secundarias debe tomar el papel de principal, puede provocar la pérdida de datos y ocurre solamente en caso de error de la base principal.