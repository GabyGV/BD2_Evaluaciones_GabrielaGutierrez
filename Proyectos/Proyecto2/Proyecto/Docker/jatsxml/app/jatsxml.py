import requests
import json
from datetime import datetime
import xmltodict
from elasticsearch import Elasticsearch
import mariadb
import pika
import os
import urllib3

### CONEXIONES
# RabbitMQ
RABBIT_USER = os.getenv("RABBIT_USER")
RABBITMQPASS = os.getenv("RABBITMQPASS")
RABBITMQ = os.getenv("RABBITMQ")
IN_QUEUE = os.getenv("IN_QUEUE")
OUT_QUEUE = os.getenv("IN_QUEUE")

# MARIADB
MARIADB_ENDPOINT = os.getenv("MARIADBENDPOINT")
MARIADB_PASSWORD = os.getenv("MARIADBPASS")
MARIADB_USER = os.getenv("MARIADB_USER")
MARIADB_DB = os.getenv("MARIADB_DB")
MARIADBPORT = os.getenv("MARIADBPORT")
# URL API de bioRXiv
API_URL = os.getenv("API_URL")
# Elastic
ELASTIC_PASSWORD = os.getenv("ELASTICPASS")
ELASTIC_ENDPOINT = os.getenv("ELASTICENDPOINT")
ELASTIC_INDEX = os.getenv("ELASTICINDEX")
ELASTIC_INDEX = os.getenv("")

HOSTNAME = os.getenv("HOSTNAME")

urllib3.disable_warnings()


# http://localhost:53644/   pass:f1a9qqwhIJ

### RECIBIR DE LA COLA

job_id = str(1)
group_id = str(0) # viene de la cola

### AGREGAR POR ACA LA MODIFICACION DE TABLAS DE MARIADB
## stage = "jatsxml-processor"
## status = "in-progress"

###AGREGAR A TABLA HISTORY CON DATOS
##stage = "jatsxml-processor"
# status = "in-progress"
# created = datetime.now()
# end = null
# message = null
# grp_id = group_id
# component = identificador del pod.

### OBTENER DOCS DE ELASTIC


###BUSCAR JATSXML
mensajeError = ""

def buscarJatsxml(details):
    try:
        urljats = details["jatsxml"]
        print(urljats)
        URL = (urljats)
        page = requests.get(URL)
        jatsxml = xmltodict.parse(page.text)
        jatsxml = json.dumps(jatsxml)
        print(jatsxml)
        statusW = "completed"
        return jatsxml
    except:
        mensajeError = "Error al bsucar jatsxml"
        print("no tiene jatsxml")
        statusW = "error"


###BORRAR ESTO LUEGO QUE ES PARA PROBAR
enlaceGeneral = "https://api.biorxiv.org/details/"

def buscarDetalles(doc):
    try:
        rel_doi = doc["rel_doi"]
        rel_site = (doc["rel_site"]).lower()
        enlaceCompleto = (enlaceGeneral + rel_site + "/" + rel_doi)
        #print(enlaceCompleto)
        URL = (enlaceCompleto)
        page = requests.get(URL)
        details = json.loads(page.text)
        details = details["collection"]
        details = details[0]
        #print(details)
        buscarJatsxml(details)
        return details
    except:
        mensajeError = "Error al extraer los detalles"
        raise ValueError(mensajeError)

def obtenerDocs():
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

obtenerDocs()

###ACTUALIZAR TABLA HISTORY
#status= statusW
# end = datetime.now()
#message = mensajeError

### ACTUALIZAR TABLA GRUPO
#status = "completed"

### Borrar el grupo de elastic