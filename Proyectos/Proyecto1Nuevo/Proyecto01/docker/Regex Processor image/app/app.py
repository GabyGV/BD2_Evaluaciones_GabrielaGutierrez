# Librerias
from tkinter import N
from tokenize import group
from elasticsearch import Elasticsearch
import mariadb
import math
import os
import json
import time
import pika
import urllib3
import re

urllib3.disable_warnings()
################## FUNCIONES NECESARIAS ##################

# Callback para consumir desde la cola
def callback(ch, method, properties, body):
    json_object = json.loads(body)
    print(body)

    # Obtiene group_id y job_id de la cola de rabbit
    groupId = json_object["group_id"]
    jobId = json_object["job_id"]

    # Obtiene archivo por group_id
    _sourceJsonWithDocs = client.get(index="groups", id=groupId)

    # Obtiene archivo por job_Id
    search_param = {"terms": {"job_id": [jobId]}}
    response = client.search(index="jobs", query=search_param)
    _sourceJson = response["hits"]["hits"][0]["_source"]

    # Se obtiene el mapeo de los campos de la expresion regularl
    fields_mapping = get_value_from_transformation(_sourceJson, "regex_config")
    docs = _sourceJsonWithDocs["_source"]["docs"]

    # Obtiene valores para formatear la expresion sql
    regexExpression = fields_mapping["regex_expression"]
    regexExpression = regexExpression.replace(" ", "")
    field = fields_mapping["field"]
    group = fields_mapping["group"]
    field_name = get_value_from_transformation(_sourceJson, "field_name")

    # Se obtiene la destination_queue
    destination_queue = get_destination_queue_transform(_sourceJson, name)

    newDocs = []

    # Recorre cada doc del group para poder aplicar la expresion regular
    for doc in docs:
        m = re.findall(regexExpression, doc[field])

        # Si hace match
        if len(m) != 0:
            doc[field_name] = m[0]
            newDocs.append(doc)
        else:
            newDocs.append(doc)

    # Update 
    body = {"doc": {"docs": newDocs}}
    client.update(
        routing=f"groups/{groupId}/_update", index="groups", id=groupId, body=body
    )
    # Envía mensajes a la cola de rabbit
    channel.queue_declare(queue=destination_queue)
    channel.basic_publish(exchange="", routing_key=destination_queue, body=json.dumps(json_object))

def limpieza_destination_queue (dic):
    dest_queue = dic
    dest_queue = dest_queue.replace("%", "", 2)
    dest_queue = dest_queue.replace("{", "")
    dest_queue = dest_queue.replace("}", "")
    return (dest_queue.split("->"))

def get_destination_queue_load(dic):
    for elem in dic["stages"]:
        if (elem["name"] == "load"):
            return elem["source_queue"]               

def get_destination_queue_transform(dic, name):
    for trans in dic["stages"][1]["transformation"]:
        search_list = limpieza_destination_queue(trans["destination_queue"])
        if (trans["name"] == name):
            if(search_list[0] == "load"):
                return get_destination_queue_load(dic)
            for elem in dic["stages"][1][search_list[1]]:
                if(elem["name"] == search_list[2]):
                    return elem["source_queue"]
    return 0

# Funcion para obtener valor de root.stages[name=transform].transformation[type=sql_transform].X
def get_value_from_transformation(dic, elem_to_be_found):
    global name
    stages = dic["stages"]
    for x in stages:
        if x["name"] == "transform":
            transformation_array = x["transformation"]
            for element in transformation_array:
                if element["type"] == "regex_transform":
                    name = element["name"]
                    return element[elem_to_be_found]

################## INICIO DEL PROGRAMA ##################

# Variables de entorno
RABBIT_MQ = os.getenv("RABBITMQ")
RABBIT_MQ_PASSWORD = os.getenv("RABBITMQPASS")

ELASTIC_PASSWORD = os.getenv("ELASTICPASS")
ELASTIC_ENDPOINT = os.getenv("ELASTICENDPOINT")
ELASTIC_INDEX = os.getenv("ELASTICINDEX")

MARIADB_ENDPOINT = os.getenv("MARIADBENDPOINT")
MARIADB_PASSWORD = os.getenv("MARIADBPASS")
MARIADB_PORT = os.getenv("MARIADBPORT")

# Conexion con ES
client = Elasticsearch(
    f"https://{ELASTIC_ENDPOINT}:9200",
    http_auth=("elastic", ELASTIC_PASSWORD),
    verify_certs=False,
)

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