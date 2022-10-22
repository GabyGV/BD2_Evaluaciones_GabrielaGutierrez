# Librerias
from elasticsearch import Elasticsearch
import mariadb
import math
import os
import json
import time
import pika
import urllib3
import re
from prometheus_client import Counter

urllib3.disable_warnings()
c = Counter('grupos_procesados', 'Cantidad de grupos procesados')
################## FUNCIONES NECESARIAS ##################

# Callback para consumir desde la cola
def callback(ch, method, properties, body):
    print(body)

    json_object = json.loads(body)
    print(json_object)
    groupId = json_object["group_id"]
    jobId = json_object["job_id"]
    x = groupId.split("-")
    c.inc()
    # Obtiene archivo por group_id
    _sourceJsonWithDocs = client.get(index="groups", id=groupId)

    # Obtiene archivo por job_Id
    search_param = {"terms": {"job_id": [jobId]}}
    response = client.search(index="jobs", query=search_param)

    # Obtiene el data_source 
    sourceJson = response["hits"]["hits"][0]["_source"]["source"]
    data_source = sourceJson["data_source"]
    
    # Se obtiene la expresion sql
    expression = get_value_from_transformation(_sourceJson, "expression")

    # Se obtiene el mapeo de los campos de la expresion sql
    fields_mapping = get_value_from_transformation(_sourceJson, "fields_mapping")
    docs = _sourceJsonWithDocs["_source"]["docs"]

    # Obtiene valores para formatear la expresion sql
    field_desc = fields_mapping["field_description"]
    field_owner = fields_mapping["field_owner"]

    # Recorre cada doc del group para poder ejecutar las expresiones
    for doc in docs:

        newDocs = {

        }

        formattedExpression = format_expression(expression, field_desc, field_owner, doc["id"])
        print("Expresion formateada", formattedExpression)

        conn = mariadb.connect(
            user="root",
            password="lJqsNUUPDn",
            host="localhost",
            port=63007,
            database=data_source,
        )

        # Ejecuta las expresiones formateadas 
        cur = conn.cursor()
        cur.execute(formattedExpression) 

        # Update de 
        client.update(routing=f"groups/{groupId}/_update",
                index="groups", id=groupId, body=body)

    # linea de codigo sacada de
    # https://stackoverflow.com/questions/5010042/mysql-get-column-name-or-alias-from-query
    # para transformar tablas de mariadb a una lista de jsons
    res = [dict((cur.description[i][0], value)
                for i, value in enumerate(row)) for row in cur.fetchall()]

    body = {"doc": {"docs": res}}
    client.update(routing=f"groups/{groupId}/_update",
                  index="groups", id=groupId, body=body)

    print(destination)

    channel.queue_declare(queue=destination)
    channel.basic_publish(exchange="", routing_key=destination, body=json.dumps(json_object))

# Funcion para limpiar valores
def limpieza (dic):
    expression = dic.replace("%", "")
    expression = expression.replace("{", "")
    expression = expression.replace("}", "")
    return (expression)

# Funcion para obtener valor de root.stages[name=transform].transformation[type=sql_transform].X
def get_value_from_transformation(dic, elem_to_be_found):
    stages = dic["stages"]
    for x in stages:
        if x["name"] == "transform":
            transformation_array = x["transformation"]
            for element in transformation_array:
                if element["type"] == "sql_transform":
                    return element[elem_to_be_found]

# Funcion para formatear la expresion sql
def format_expression(expression, field_description, field_owner, doc_id):
    # Formatear expresión
    expression = expression.replace("field_description", field_description)
    expression = expression.replace("field_owner", field_owner)
    expression = expression.replace("doc_field", str(doc_id))
    return limpieza(expression)

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
    f"https://localhost:63469",
    http_auth=("elastic", "M6x522ObDFs6Yl5i2R878lHz"),
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
    credentials = pika.PlainCredentials("user", "KOXlRoUplntLFOQP")
    parameters = pika.ConnectionParameters(host="localhost", port=63760, credentials=credentials) 
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=source_queue)

    # Consumir mensaje 
    channel.basic_consume(queue=source_queue, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()



#if (jobs["stages"][0]["name"]=="extract"):
#    source_queue = get_value_from_transformation(jobs, "source_queue")
#    expression = get_value_from_transformation(jobs, "expression")
#
#    print("source queue: ", source_queue)
#   print("expression: ", expression)



