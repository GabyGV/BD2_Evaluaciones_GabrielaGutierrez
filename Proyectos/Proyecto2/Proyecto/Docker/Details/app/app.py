import requests
import json
from elasticsearch import Elasticsearch
import mariadb
import pika
import os
import urllib3
import time
enlaceGeneral = "https://api.biorxiv.org/details/"

# CONEXIONES
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


def callback(ch, method, properties, body):
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

    client = Elasticsearch(
        f"http://localhost:61707/"
    )
    searchParam = {"terms": {"group_id": grpNumber}}
    response = client.search(index="groups", query=searchParam)
    _sourceJson = response["hits"]["hits"][0]["_source"]

    def modifyJobs(id):
        try:
            cur.execute(
                f"UPDATE groups SET _status = 'inprogress', stage = 'details-downloader'  WHERE grp_number = {id}")
            conn.commit()

        except mariadb.Error as e:
            print(f"Error MariaDB: {e}")

        return

    def insertHistory():
        cur.execute(
            f"""
            INSERT INTO history (created_time,stage,_status,grp_id,component)
            VALUES (
                    NOW(),
                    "details-downloader",
                    "inprogress",
                    {grpNumber},
                    '{HOSTNAME}'
                    )""")
        conn.commit()
        return
    def updateError():#falta
        cur.execute(
            f"""
            UPDATE history 
            SET _status = 'error',
                end_time = NOW(),
                message = '{mensajeError}'
            WHERE grp_id = {grpNumber}
            """)
        conn.commit()
        return

    def updateComplete():
        cur.execute(
            f"""
            UPDATE groups 
            SET _status = 'completed'
            WHERE grp_number = {grpNumber}
            """)
        conn.commit()

        cur.execute(
            f"""
            UPDATE history 
            SET _status = 'completed',
                end_time = NOW()
            WHERE grp_id = {grpNumber}
            """)
        conn.commit()
        return

    modifyJobs(grpNumber)
    insertHistory()

    # regresar doc de elastic

    try:

        docs = _sourceJson["doc"]["docs"]
        newDocs = []
        for doc in docs:  # cada doc del grupo
            rel_doi = doc["rel_doi"]
            rel_site = (doc["rel_site"]).lower()
            enlaceCompleto = (enlaceGeneral + rel_site + "/" + rel_doi)
            URL = (enlaceCompleto)

            page = requests.get(URL)
            details = json.loads(page.text)
            details = details["collection"]
            print(details)

            print("llego a procesar los details")

            doc["details"] = details

            newDocs.append(doc)

        body = {"doc": {"docs": newDocs}}

        client.update(
            routing=f"groups/{grpNumber}/_update", index="groups", id=grpNumber, body=body)

        if statusW != "error":
            updateComplete()
        else:
            updateError()


        channel.queue_declare(queue='jastxm')
        channel.basic_publish(
            exchange="", routing_key="jastxm", body=json.dumps(json_object)
        )
        statusW = "completed"
    except:
        mensajeError = "Error al extraer de la página"
        statusW = "error"









while True:

    credentials = pika.PlainCredentials("user", "ekhVwr5eTRQRnsTN")
    parameters = pika.ConnectionParameters(
        host="localhost", credentials=credentials, port=55876)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue="detail_downloader")
    channel.basic_consume(queue="detail_downloader",
                          on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

    print("No hay documentos")
    time.sleep(3)
