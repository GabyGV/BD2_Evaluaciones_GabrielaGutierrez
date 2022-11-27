import mariadb
import urllib3
import pika
import math
import os
import requests
import json
from datetime import datetime
import time

# RabbitMQ
RABBIT_USER = os.getenv("RABBIT_USER")
RABBITMQPASS = os.getenv("RABBITMQPASS")
RABBITMQ = os.getenv("RABBITMQ")
IN_QUEUE = os.getenv("IN_QUEUE")
OUT_QUEUE = os.getenv("OUT_QUEUE")

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


def searchJobs():
    try:
        cur.execute(
            "SELECT id,grp_size, _status FROM jobs")

        total = cur.fetchall()
        for id, grp_size, _status in total:
            print(id, grp_size, _status)
            if _status == "new":
                print(id, grp_size)
                return [id, grp_size]
        return None

    except mariadb.Error as e:
        print(f"Error MariaDB: {e}")


def modifyJobs(id):
    try:
        cur.execute(
            f"UPDATE jobs SET _status = 'inprogress', loader = '{HOSTNAME}'  WHERE id = {id}")
        conn.commit()
    except mariadb.Error as e:
        print(f"Error MariaDB: {e}")


def getDataURL():
    URL = (API_URL)
    page = requests.get(URL)
    docs = json.loads(page.text)
    docs = docs['messages']
    return docs[0]


while True:

    credentials = pika.PlainCredentials(RABBIT_USER, RABBITMQPASS)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ, credentials=credentials)
    connection = pika.BlockingConnection(parameters)

    try:
        conn = mariadb.connect(
            user=MARIADB_USER,
            password=MARIADB_PASSWORD,
            host=MARIADB_ENDPOINT,
            port=3306,
            database=MARIADB_DB,
        )
        cur = conn.cursor()

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")

    jobs = searchJobs()
    print(jobs)
    if jobs != None:
        channel = connection.channel()
        channel.queue_declare(queue=OUT_QUEUE)
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
            cur.execute(
                f"""
                INSERT INTO groups (id_job,created_time,stage,grp_number,offset_number) 
                VALUES ({id}, 
                        NOW(), 
                        '{HOSTNAME}',
                        {grp_number},
                        {offset_number}
                        )""")
            conn.commit()

            newGroup = {
                "id_job": f"{id}",
                "grp_number": f"{grp_number}",
            }
            channel.basic_publish(
                exchange="", routing_key=OUT_QUEUE, body=json.dumps(newGroup)
            )
            grp_number += 1
            offset_number += grp_size
        connection.close()
    else:
        print("Without jobs")
    time.sleep(5)
