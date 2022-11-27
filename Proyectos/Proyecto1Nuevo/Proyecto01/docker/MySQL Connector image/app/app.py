# Librerias
from elasticsearch import Elasticsearch
import mariadb
import os
import json
import time
import pika
import urllib3

urllib3.disable_warnings()


def callback(ch, method, properties, body):
    print(body)

    json_object = json.loads(body)
    print(json_object)
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
            destination_queue = x["destination_queue"]
    print(destination_queue)

    destination = get_destination_queue_extract(_sourceJson, destination_queue)

    conn = mariadb.connect(
        user="root",
        password=MARIADB_PASSWORD,
        host=MARIADB_ENDPOINT,
        port=3306,
        database=data_source,
    )
    cur = conn.cursor()
    cur.execute(newExpression)
    # linea de codigo sacada de
    # https://stackoverflow.com/questions/5010042/mysql-get-column-name-or-alias-from-query
    # para transformar tabblas de mariadb a una lista de jsons
    res = [
        dict((cur.description[i][0], value) for i, value in enumerate(row))
        for row in cur.fetchall()
    ]

    body = {"doc": {"docs": res}}
    client.update(
        routing=f"groups/{groupId}/_update", index="groups", id=groupId, body=body
    )

    print(destination)

    channel.queue_declare(queue=destination)
    channel.basic_publish(
        exchange="", routing_key=destination, body=json.dumps(json_object)
    )


def limpieza(dic):
    dest_queue = dic
    dest_queue = dest_queue.replace("%", "", 2)
    dest_queue = dest_queue.replace("{", "")
    dest_queue = dest_queue.replace("}", "")

    print("Solamente el destination_queue limpio: ", dest_queue)
    return dest_queue.split("->")


def get_destination_queue_load(dic):
    for elem in dic["stages"]:
        if elem["name"] == "load":
            print(elem["source_queue"])
            return elem["source_queue"]


def get_destination_queue_extract(dic, destination):
    search_list = limpieza(destination)
    for element in search_list:
        for defi in dic["stages"]:
            if defi["name"] == "load":
                return get_destination_queue_load(dic)
            if defi["name"] == search_list[0]:
                for trans in defi[search_list[1]]:
                    print(trans)
                    if trans["name"] == search_list[2]:
                        return trans["source_queue"]


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
# update
while True:
    try:

        search_param = {"terms": {"job_id": ["inprogress"]}}
        client = Elasticsearch(
            f"https://{ELASTIC_ENDPOINT}:9200/",
            http_auth=("elastic", ELASTIC_PASSWORD),
            verify_certs=False,
        )

        search_param = {"terms": {"status": ["inprogress"]}}


        response = client.search(index="jobs", query=search_param)

        _sourceJson = response["hits"]["hits"][0]["_source"]
        stages = _sourceJson["stages"]
        for x in stages:
            if x["name"] == "extract":
                source_queue = x["source_queue"]
        print(source_queue)
        credentials = pika.PlainCredentials("user", RABBIT_MQ_PASSWORD)
        parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=source_queue)
        channel.basic_consume(queue=source_queue, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
    except:
        print("No hay documentos")
    
    time.sleep(3)









    