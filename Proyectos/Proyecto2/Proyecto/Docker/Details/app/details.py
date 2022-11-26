import requests
import json
from datetime import datetime

### RECIBIR DE LA COLA

job_id = str(1)
group_id = str(0) # viene de la cola

### AGREGAR POR ACA LA MODIFICACION DE TABLAS DE MARIADB
## stage = "downloader"
## status = "in-progress"

###AGREGAR A TABLA HISTORY CON DATOS
##stage = "details-dowloader"
# status = "in-progress"
# created = datetime.now()
# end = null
# message = null
# grp_id = group_id
# component = identificador del pod.

### Obtener el grupo de elastic 


enlaceGeneral = "https://api.biorxiv.org/details/"
mensajeError = ""

def buscarDetalles(doc):
    try:
        rel_doi = doc["rel_doi"]
        rel_site = (doc["rel_site"]).lower()
        enlaceCompleto = (enlaceGeneral + rel_site + "/" + rel_doi)
        print(enlaceCompleto)
        URL = (enlaceCompleto)
        page = requests.get(URL)
        details = json.loads(page.text)
        details = details["collection"]
        details = details[0]
        print(details)
        statusW = "completed"
        return details
    except:
        mensajeError = "Error al extraer los detalles"
        statusW = "error"
        raise ValueError(mensajeError)

###borrar esta parte que es solo para pruebas
try:
    URL = ("https://api.biorxiv.org/covid19/" + group_id)
    page = requests.get(URL)

    docs = json.loads(page.text)
    docs = docs['collection']
### 

    for doc in docs: #cada doc del grupo de elastic
        print("\n")
        #print(doc)
        buscarDetalles(doc) 
    statusW = "completed"
except:
    statusW = "error"

###ACTUALIZAR TABLA HISTORY
#status= statusW
# end = datetime.now()
#message = mensajeError

### ACTUALIZAR TABLA GRUPO
#status = "completed"

### agregar el mensaje en la cola

cola = {"id_job": job_id, "grp_id" : group_id}