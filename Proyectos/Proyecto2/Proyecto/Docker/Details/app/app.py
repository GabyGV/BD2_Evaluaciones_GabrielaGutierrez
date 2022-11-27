import requests
import json
from elasticsearch import Elasticsearch
import mariadb
import pika
import os
import urllib3
import time


globalArray = []
grp_size = 0
job_id = str(0)
group_id = str(0) # viene de la cola
enlaceGeneral = "https://api.biorxiv.org/details/"
mensajeError = ""

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

def callback(ch, method, properties, body):
    global grp_size
    global globalArray
    print(body)

    print("entro un msj")
    json_object = json.loads(body)
    grpNumber = json_object["grp_number"]
    idJob = json_object["id_job"]

    conn = mariadb.connect(
        user="root",
        password="f1a9qqwhIJ",
        host="localhost",
        port=55957,
        database="workload",
    )
    cur = conn.cursor()

    def searchJobData(idJob):
        cur.execute(
            f"SELECT grp_size FROM jobs WHERE id = {idJob}")

        total = cur.fetchone()
        print(total)
        for x in total:
            return x
        return None

    def modifyJobs(id):
        try:
            cur.execute(
                f"UPDATE groups SET _status = 'inprogress', stage = 'detailsDownloader'  WHERE grp_number = {id}")
            conn.commit()

        except mariadb.Error as e:
            print(f"Error MariaDB: {e}")

        return

    def searchGroupId(id):
        cur.execute(
            f"SELECT id FROM groups WHERE grp_number = {id}")

        total = cur.fetchone()
        for id in total:
            return id
        return None

    groupId = searchGroupId(idJob)

    def insertHistory():
        cur.execute(
            f"""
            INSERT INTO history (created_time,stage,_status,grp_id,component) 
            VALUES ( 
                    NOW(),
                    "detailsDowloader",
                    "inprogress",
                    {groupId},
                    '{HOSTNAME}'
                    )""")
        conn.commit()
        return

    def updateError():
        cur.execute(
            f"""
            INSERT INTO history (created_time,stage,_status,grp_id,component) 
            VALUES ( 
                    NOW(),
                    "detailsDowloader",
                    "inprogress",
                    {groupId},
                    HOSTNAME
                    )""")
        conn.commit()
        return

    def updateComplete():
        cur.execute(
            f"""
            INSERT INTO history (created_time,stage,_status,grp_id,component) 
            VALUES ( 
                    NOW(),
                    "detailsDowloader",
                    "completed",
                    {groupId[0]},
                    HOSTNAME
                    )""")
        conn.commit()
        return

    def agregarDocElastic():
        return

    modifyJobs(grpNumber)
    insertHistory()
    if grp_size == 0:
        groupSize = searchJobData(idJob)
        grp_size = groupSize
    try:
        ###regresar doc de elastic
        docs = {""}

        for doc in docs:  # cada doc del grupo
            rel_doi = doc["rel_doi"]
            rel_site = (doc["rel_site"]).lower()
            enlaceCompleto = (enlaceGeneral + rel_site + "/" + rel_doi)
            URL = (enlaceCompleto)

            page = requests.get(URL)
            details = json.loads(page.text)
            details = details["collection"]
            details = details[0]
            print(details)
 
            print("llego a procesar los details")

            title = doc["title"]
            rel_authors = doc["authors"]
            category = doc["category"]
            rel_abs = doc["abstract"]
            rel_doi = doc["doi"]
            jatsxml = doc["jatsxml"]

            jsonDoc = {}
            jsonDoc["title"] = title
            jsonDoc["athors"] = rel_authors
            jsonDoc["category"] = category
            jsonDoc["abstract"] = rel_abs
            jsonDoc["doi"] = rel_doi
            jsonDoc["jatsxml"] = jatsxml
            print(len(globalArray))
            print(grp_size)

            if len(globalArray) < grp_size:

                globalArray.append(jsonDoc)
            else:
                newGroup = {
                    "job_id": f"{idJob}",
                    "group_id": f"{groupId}",
                    "doc": {"docs": globalArray}}
                globalArray = []
                client.index(
                    routing=f"jobs/_create/{groupId}", id=groupId, index="groups", document=newGroup)
                globalArray.append(jsonDoc)

        statusW = "completed"
    except:
        mensajeError = "Error al extraer de la página"
        statusW = "error"

    # if statusW != "error":

    # else:
      #  updateError(grpNumber)##########################################################falta

    channel.queue_declare(queue='detail')
    channel.basic_publish(
        exchange="", routing_key="detail", body=json.dumps(json_object)
    )



while True:
    client = Elasticsearch(
        f"http://localhost:61707/"
    )

    if client.indices.exists(index="groups") != True:
        client.indices.create(index="groups")
        print("No existe /groups")
    else:
        print("Si existe /groups")

    credentials = pika.PlainCredentials("user", "ekhVwr5eTRQRnsTN")
    parameters = pika.ConnectionParameters(
        host="localhost", credentials=credentials, port=55876)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue="downloader")
    channel.basic_consume(queue="downloader",
                          on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

    print("No hay documentos")
    time.sleep(3)
