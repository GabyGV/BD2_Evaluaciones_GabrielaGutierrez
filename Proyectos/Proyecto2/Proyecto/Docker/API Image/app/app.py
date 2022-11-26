# Librerias
from flask import Flask

import json

import mariadb
import math
import os
import pika
import urllib3

urllib3.disable_warnings()


# Variables de entorno
#USUARIO Y PASSWORD DE RABBITMQ
RABBIT_MQ = os.getenv("RABBITMQ")
RABBIT_MQ_PASSWORD = os.getenv("RABBITMQPASS")

#USUARIO, PASSWORD E INDICE DE ELASTICSEARCH
ELASTIC_PASSWORD = os.getenv("ELASTICPASS")
ELASTIC_ENDPOINT = os.getenv("ELASTICENDPOINT")
ELASTIC_INDEX = os.getenv("ELASTICINDEX")

#USUARIO, PASSWORD Y PUERTO DE MARIADB
MARIADB_ENDPOINT = os.getenv("MARIADBENDPOINT")
MARIADB_PASSWORD = os.getenv("MARIADBPASS")
MARIADB_PORT = os.getenv("MARIADBPORT")

# Inicializa el API
app = Flask(__name__)

@app.route('/app/getData')
def getMessage():

    try:
        conn = mariadb.connect(
            user="root",
            password="lJqsNUUPDn",
            host="localhost",
            port=57531,
            database="car_db",
        )

        cur = conn.cursor()
        cur.execute(f"SELECT * from car")

        # Código de https://stackoverflow.com/questions/43796423/python-converting-mysql-query-result-to-json
        # Convierte el resultado del select en un json
        row_headers=[x[0] for x in cur.description] #this will extract row headers
        rv = cur.fetchall()
        json_data=[]
        for result in rv:
                json_data.append(dict(zip(row_headers,result)))
        return json.dumps(json_data)

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return (f"Error connecting to MariaDB Platform: {e}")

@app.route('/app/setData/<name>', methods=["POST"])
def setMessage(name):

    try:
        conn = mariadb.connect(
            user="root",
            password="lJqsNUUPDn",
            host="localhost",
            port=57531,
            database="people_db",
        )

        cur = conn.cursor()
        cur.execute(f"INSERT INTO persona (cedula, nombre) VALUES (?, ?)", (407, name))
        conn.commit()

        return name

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return (f"Error connecting to MariaDB Platform: {e}")

# Corre el API
app.run(debug=True)

##http://127.0.0.1:5000/app/getMessage