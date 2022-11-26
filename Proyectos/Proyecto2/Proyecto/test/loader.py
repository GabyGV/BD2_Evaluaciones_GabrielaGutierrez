import mariadb
import urllib3
import pika
import math
import os
import requests
import json
from datetime import datetime

prueba = '"loader_pod"'
# RabbitMQ
RABBIT_MQ = os.getenv("RABBITMQ")
RABBIT_ENDPOINT = os.getenv("RABBITMQPASS")
RABBIT_MQ = os.getenv("RABBITMQPASS")
IN_QUEUE = os.getenv("IN_QUEUE")
OUT_QUEUE = os.getenv("IN_QUEUE")

# MARIADB
MARIADB_ENDPOINT = os.getenv("MARIADBENDPOINT")
MARIADB_PASSWORD = os.getenv("MARIADBPASS")
MARIADB_USER = os.getenv("MARIADB")
MARIADB_DB = os.getenv("jobs")

# URL API de bioRXiv
API_URL = os.getenv("API_URL")
# Elastic
ELASTIC_PASSWORD = os.getenv("ELASTICPASS")
ELASTIC_ENDPOINT = os.getenv("ELASTICENDPOINT")
ELASTIC_INDEX = os.getenv("ELASTICINDEX")
ELASTIC_INDEX = os.getenv("")

urllib3.disable_warnings()


# http://localhost:53644/   pass:f1a9qqwhIJ


try:
    conn = mariadb.connect(
        user="root",
        password="f1a9qqwhIJ",
        host="localhost",
        port=53644,
        database="workload",
    )
    cur = conn.cursor()

except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")



credentials = pika.PlainCredentials("user", "CtcvCyvsF7CPbgSk")
parameters = pika.ConnectionParameters(
    host="localhost", credentials=credentials, port=61513
)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue="prueba")


def searchJobs():
    try:
        cur.execute(
            "SELECT id,grp_size FROM jobs WHERE _status = 'inprogress' ")
        for id, grp_size in cur:
            return [id, grp_size]

    except mariadb.Error as e:
        print(f"Error MariaDB: {e}")


def modifyJobs(id):
    print(id)
    try:
        cur.execute(
            f"UPDATE jobs SET _status = 'inprogress', loader = {prueba}  WHERE id = {id}")
        conn.commit()
        print("hola")

    except mariadb.Error as e:
        print(f"Error MariaDB: {e}")


def getDataURL():
    URL = ("https://api.biorxiv.org/covid19/0")
    page = requests.get(URL)
    docs = json.loads(page.text)
    docs = docs['messages']
    return docs[0]


jobs = searchJobs()

if jobs != None:
    id = jobs[0]
    grp_size = jobs[1]

    modifyJobs(id)

    docs = getDataURL()
    total = docs['total']

    counter = math.ceil(total/grp_size)
    grp_number = 1
    offset_number = 0
    for x in range(counter):
        now = datetime.now()
        now = now.strftime("%Y-%m-%d")
        print(now)
        
        cur.execute(
            f"""
            INSERT INTO groups (id_job,created_time,stage,grp_number,offset_number) 
            VALUES ({id}, 
                    NOW(), 
                    "loader",
                    {grp_number},
                    {offset_number})""")
        conn.commit()

        newGroup = {
                    "id_job": f"{id}",
                    "grp_number": f"{grp_number}",
                    }
        channel.basic_publish(
            exchange="", routing_key="prueba", body=json.dumps(newGroup)
        )
        grp_number += 1
        offset_number += grp_size