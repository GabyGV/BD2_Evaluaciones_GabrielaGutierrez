import requests
import json
from datetime import datetime
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


while True:
    ################## OBTENER VALORES DEL JSON ################## 

    # Busqueda de archivo en ES
    search_param = {"terms": {"status": ["inprogress"]}} 
    response = client.search(index="jobs", query=search_param)

    # Se obtiene el source del json
    _sourceJson = response["hits"]["hits"][0]["_source"]

    # Se obtiene el source queue a partir del json
    source_queue = get_value_from_transformation(_sourceJson, "source_queue")

    ################## Conexion con RabbitMQ ##################
    credentials = pika.PlainCredentials("user", RABBIT_MQ_PASSWORD)
    parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials) 
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=source_queue)

    # Consumir mensaje 
    channel.basic_consume(queue=source_queue, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
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