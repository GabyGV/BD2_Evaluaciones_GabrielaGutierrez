# Librerias
from elasticsearch import Elasticsearch
import mariadb
import math
import os
import json
import time
import pika
import urllib3

urllib3.disable_warnings()


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
    f"https://{ELASTIC_ENDPOINT}:9200/",
    http_auth=("elastic", ELASTIC_PASSWORD),
    verify_certs=False,
)


while True:

    # Verificar Indices Jobs y Group--------------------------------------------
    if client.indices.exists(index="jobs") != True:
        client.indices.create(index="jobs")
        print("No existe /jobs")
    else:
        print("Si existe /jobs")

    if client.indices.exists(index="groups") != True:
        client.indices.create(index="groups")
        print("No existe /groups")

    else:
        print("Si existe /groups")

    # Parametros de busca-------------------------------------------
    search_param = {"terms": {"status": ["new"]}}
    print("conexion con elastic")

    response = client.search(index="jobs", query=search_param)
    # Verifica que hayan documentos con el status "new"
    try:
        print("hola")
        hitsJson = response["hits"]["hits"][0]
        id = hitsJson["_id"]
        _sourceJson = response["hits"]["hits"][0]["_source"]
        job_id = _sourceJson["job_id"]
        sourceJson = response["hits"]["hits"][0]["_source"]["source"]
        data_sources = response["hits"]["hits"][0]["_source"]["data_sources"]
        expression = sourceJson["expression"]
        gpr_size = int(sourceJson["grp_size"])
        data_source = sourceJson["data_source"]
        stages = _sourceJson["stages"]
        for x in stages:
            if x["name"] == "extract":
                source_queue = x["source_queue"]
        body = {"doc": {"status": "inprogress"}}

        client.update(routing=f"jobs/{id}/_update", index="jobs", id=id, body=body)
        print(client.update(index="jobs", id=id, body=body))

        print("Se actualizo el documento")
        print(MARIADB_PASSWORD)
        print(MARIADB_ENDPOINT)
        print(MARIADB_PORT)
        print(data_source)
        print(gpr_size)
        print(expression)
        print(source_queue)

        try:
            conn = mariadb.connect(
                user="root",
                password=MARIADB_PASSWORD,
                host=MARIADB_ENDPOINT,
                port=3306,
                database=data_source,
            )
            print("Se conecto con mariaDB")
            cur = conn.cursor()
            cur.execute(f"SELECT COUNT(1) FROM ({expression}) AS a")
            total = cur.fetchone()
            print(int(total[0]))
            totalDocs = math.ceil(total[0] / gpr_size)
            initialValue = 0
            print("calculo el valor")
            credentials = pika.PlainCredentials("user", RABBIT_MQ_PASSWORD)
            parameters = pika.ConnectionParameters(
                host=RABBIT_MQ, credentials=credentials
            )
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare(queue=source_queue)
            print("se establecio conexion con rabit")
            for x in range(totalDocs):
                offset = f"{job_id}-{initialValue}"
                newGroup = {
                    "job_id": f"{job_id}",
                    "group_id": f"{job_id}-{initialValue}",
                }
                add = client.index(
                    routing=f"jobs/_create/{offset}",id=offset, index="groups", document=newGroup
                )
                channel.basic_publish(
                    exchange="", routing_key=source_queue, body=json.dumps(newGroup)
                )
                initialValue += gpr_size
                print(newGroup)
            connection.close()

            print("se crearon los groups")
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")

    except:
        print("no hay documentos a processar")
    time.sleep(8)


# 1000 elementos / 100 = 10
# 0 hasta 99
# 100 hasta 199
# ...
# job606-0
# job606-100

"""
response = response["hits"]["hits"]
response = json.dumps(response[0])
y = json.loads(response)

"""

##Conectar con MAriaDB
##enviar el archivo a rabbit
##update del doc


"""
#Parte de MariaDB
def get_field_info(cur):
    field_info = mariadb.fieldinfo()
    field_info_text = []
    for column in cur.description:
      column_name = column[0]
      column_type = field_info.type(column)
      column_flags = field_info.flag(column)

      field_info_text.append(f"{column_name}: {column_type} {column_flags}")

    return field_info_text

try:
    conn = mariadb.connect(
        user="root",
        password="l9mXQYS6eL",
        host="127.0.0.1",
        port=50908,
        database="people_db"
    )
    cur = conn.cursor()
    cur.execute("SELECT Cedula FROM Person")
    row= cur.fetchall()
    print(*row) 
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    
"""
# Get Cursor


####
# Listo el update


####
# falta el total de registros a migrar
