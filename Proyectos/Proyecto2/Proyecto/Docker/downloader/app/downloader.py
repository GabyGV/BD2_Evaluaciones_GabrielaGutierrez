import requests
import json
from datetime import datetime
from elasticsearch import Elasticsearch
import mariadb
import pika

### RECIBIR DE LA COLA

job_id = str(1)
group_id = str(1) # viene de la cola

### AGREGAR POR ACA LA MODIFICACION DE TABLAS DE MARIADB
## stage = "downloader"
## status = "in-progress"

###AGREGAR A TABLA HISTORY CON DATOS
##stage = "dowloader"
# status = "in-progress"
# created = datetime.now()
# end = null
# message = null
# grp_id = group_id
# component = identificador del pod.


###Extraer docs
mensajeError = ""

try:
    URL = ("https://api.biorxiv.org/covid19/" + group_id)
    page = requests.get(URL)

    docs = json.loads(page.text)
    docs = docs['collection']

    for doc in docs: #cada doc del grupo
        print("\n")
        print(doc)
    
    statusW = "completed"
except:
    mensajeError = "Error al extraer de la página"
    statusW = "error"



### AGREGAR A ELASTIC

### ACTUALIZAR TABLA HISTORY
# status = statusW
# end = datetime.now()
# message = mensajeError

### ACTUALIZAR TABLA GRUPO
#status = "completed"

### agregar el mensaje en la cola

cola = {"id_job": job_id, "grp_id" : group_id}