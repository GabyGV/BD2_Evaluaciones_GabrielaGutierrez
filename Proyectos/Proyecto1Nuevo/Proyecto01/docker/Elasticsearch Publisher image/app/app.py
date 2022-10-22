# Librerias
from elasticsearch import Elasticsearch
import math
import os
import json
import time
import pika
import urllib3
import re

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
    _sourceJsonWithDocs = client.get(index="groups", id=groupId)
    
    docs = _sourceJsonWithDocs["_source"]['docs']
    _sourceJson = response["hits"]["hits"][0]["_source"]
    stages = _sourceJson["stages"]
    for x in stages:
        if x["name"] == "load":
       
            index = x["index_name"]

    if client.indices.exists(index=index) != True:
        client.indices.create(index=index)
        print("No existe /jobs")
    else:
        print("Si existe /jobs")
    for doc in docs:
        docId = doc["id"]
        client.index(
                    routing=f"jobs/_create/{docId}",id=docId, index=index, document=doc
                )
    print(groupId)
    client.delete(index="groups",id=groupId)
# Conexion con ES
RABBIT_MQ = os.getenv("RABBITMQ")
RABBIT_MQ_PASSWORD = os.getenv("RABBITMQPASS")

ELASTIC_PASSWORD = os.getenv("ELASTICPASS")
ELASTIC_ENDPOINT = os.getenv("ELASTICENDPOINT")
ELASTIC_INDEX = os.getenv("ELASTICINDEX")

EXTRACT_QUEUE = os.getenv("EXTRACTQUEUE")

search_param = {"terms": {"status": ["inprogress"]}}
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
    if x["name"] == "load":
       
        source_queue = x["source_queue"]
        print(source_queue)
print(source_queue)
credentials = pika.PlainCredentials("user", RABBIT_MQ_PASSWORD)
parameters = pika.ConnectionParameters(
    host=RABBIT_MQ,
    credentials=credentials
)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=source_queue)
channel.basic_consume(queue=source_queue,
                        on_message_callback=callback, auto_ack=True)
channel.start_consuming()

print("hola")
