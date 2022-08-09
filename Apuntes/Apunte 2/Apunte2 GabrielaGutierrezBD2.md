# Apuntes: Clase 2

### _Bases de Datos II_

>Semestre 2, Semana 1, Fecha: 29 de Julio, 2022

>Creado por: Gabriela Gutiérrez - 2019024089

### Tema:
- Kubernetes

## ¿Qué es Kubernetes?
Plataforma para automatizar la implementación, el escalado y la administración de aplicaciones en contenedores(pods).

_**Contenedores**_: agrupan el programa con todos los archivos necesarios para su ejecución independiente del sistema operativo -> define reglas sobre las cuales corre el código.

![Contenedores](https://d33wubrfki0l68.cloudfront.net/e7b766e0175f30ae37f7e0e349b87cfe2034a1ae/3e391/images/docs/why_containers.svg)

_**Deployment**_: Define el comportamiento y estado de los pods.
- Stateful: mantiene el estado
- Stateless: no mantiene su estado

_**Service**_: describe como se accesa a las aplicaciones, tal como a un conjunto de pods. Puede describir puertos (**ClusterIP**) y balanceadores de carga.

_**Scheduler**_: Por cada pod que descubre se vuelve responsable de encontrar el mejor nodo para que se ejecute ese pod.

_**Namespaces**_: clústeres virtuales respaldados por el mismo clúster físico. Pensados para utilizarse en entornos con muchos usuarios distribuidos entre múltiples equipos, o proyectos.

_**DaemonSets**_: un pod que es ejecutado por todos (o algunos) de los nodos.

## Comandos

### Sintaxis:

```sh
kubectl [command] [TYPE] [NAME] [flags]
```

Donde:
- command: operación a realizar
- TYPE: tipo de recurso
- Name: nombre del recurso.
- flags: banderas opcionales

### Algunos comandos de ejemplo:

GET
```sh
kubectl get pods
kubectl get namespaces
```
CREATE NAMESPACE
```sh
kubectl create namespace [NAME]
```
DELETE
```sh
kubectl delete –f ([-f FILENAME] | TYPE [(NAME | -l label | --all)])
```
CLUSTER INFO
```sh
kubectl cluster-info [flags]
```



\* Imagen y comandos tomados de la documentación oficial de [Kubernetes](https://kubernetes.io/docs/home/)