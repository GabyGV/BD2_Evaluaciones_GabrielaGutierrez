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

urllib3.disable_warnings()


def callback(ch, method, properties, body):

    json_object = json.loads(body)
    groupId = json_object["group_id"]
    jobId = json_object["job_id"]
    x = groupId.split("-")
    search_param = {"terms": {"job_id": [jobId]}}
    response = client.search(index="jobs", query=search_param)
    _sourceJson = response["hits"]["hits"][0]["_source"]
    sourceJson = response["hits"]["hits"][0]["_source"]["source"]
    data_source = sourceJson["data_source"]
    expression = sourceJson["expression"]
    gpr_size = int(sourceJson["grp_size"])
    newExpression = f"{expression} LIMIT {x[1]},{gpr_size}"
    stages = _sourceJson["stages"]
    for x in stages:
            if x["name"] == "extract":
                destination_queue = x["source_queue"]
    

    conn = mariadb.connect(
    user="root",
    password=MARIADB_PASSWORD,
    host=MARIADB_ENDPOINT,
    port=3306,
    database=data_source,
)
    cur = conn.cursor()
    cur.execute(newExpression)
    #linea de codigo sacada de 
    #https://stackoverflow.com/questions/5010042/mysql-get-column-name-or-alias-from-query
    #para transformar tabblas de mariadb a una lista de jsons
    res = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]

    body = {"doc": res}
    client.update(routing=f"groups/{groupId}/_update", index="groups", id=groupId, body=body)

    channel.queue_declare(queue="extract")


    


# Variables de entorno
RABBIT_MQ = os.getenv("RABBITMQ")
RABBIT_MQ_PASSWORD = os.getenv("RABBITMQPASS")

ELASTIC_PASSWORD = os.getenv("ELASTICPASS")
ELASTIC_ENDPOINT = os.getenv("ELASTICENDPOINT")
ELASTIC_INDEX = os.getenv("ELASTICINDEX")

MARIADB_ENDPOINT = os.getenv("MARIADBENDPOINT")
MARIADB_PASSWORD = os.getenv("MARIADBPASS")
MARIADB_PORT = os.getenv("MARIADBPORT")

EXTRACT_QUEUE = os.getenv("EXTRACTQUEUE")
# Conexion con ES

search_param = {"terms": {"job_id": ["new"]}}
client = Elasticsearch(
    f"https://{ELASTIC_ENDPOINT}:9200/",
    http_auth=("elastic", ELASTIC_PASSWORD),
    verify_certs=False,
)


print("conexion con elastic")

credentials = pika.PlainCredentials("user", "RhUiJZ34bHYuNKWW")
parameters = pika.ConnectionParameters(
    host="localhost", port=56136, credentials=credentials
)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue="extract")
channel.basic_consume(queue="extract", on_message_callback=callback, auto_ack=True)
channel.start_consuming()

channel.queue_delete()
"""
#Parametros de busca-------------------------------------------

    response = client.search(index="jobs", query=search_param)
#Verifica que hayan documentos con el status "new"
    try:
        print('hola')
        hitsJson = response["hits"]["hits"][0]
        id = hitsJson["_id"]
        _sourceJson = response["hits"]["hits"][0]["_source"]
        job_id = _sourceJson["job_id"]
        sourceJson = response["hits"]["hits"][0]["_source"]["source"]
        data_sources = response["hits"]["hits"][0]["_source"]["data_sources"]
        expression = sourceJson['expression']
        gpr_size = int(sourceJson['grp_size'])
        data_source = sourceJson['data_source']
        stages = _sourceJson["stages"]
        for x in stages:
            if x["name"] == "extract":
                source_queue = x["source_queue"]
        body = {
        "doc":{
        "status" : "inprogress"}}

        client.update(routing=f'jobs/{id}/_update', index="jobs", id=id,body=body)
        print(client.update(index='jobs',id=id, body=body))

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
            password = MARIADB_PASSWORD,
            host=MARIADB_ENDPOINT,
            port=3306,
            database= data_source
        )
            print("Se conecto con mariaDB")
            cur = conn.cursor()
            cur.execute(f"SELECT COUNT(1) FROM ({expression}) AS a")
            total= cur.fetchone()
            print(int(total[0]))
            totalDocs =math.ceil(total[0]/gpr_size)
            initialValue = 0
            print("calculo el valor")
            credentials = pika.PlainCredentials("user",RABBIT_MQ_PASSWORD)
            parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials)
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare(queue=source_queue)
            print("se establecio conexion con rabit")
            for x in range(totalDocs):
                newGroup = {
                    "job_id": f"{job_id}",
                    "group_id":  f"{job_id}-{initialValue}"
                }
                add = client.index(routing=f'jobs/_create',index="groups", document=newGroup)
                channel.basic_publish(exchange='', routing_key=source_queue, body=json.dumps(newGroup))
                initialValue += gpr_size
                print(newGroup)
            connection.close()

            print("se crearon los groups")
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")


    except:
        print("no hay documentos a processar")
    time.sleep(8)






"""


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
