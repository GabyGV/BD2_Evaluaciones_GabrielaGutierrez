# Librerias
from flask import Flask
import json
import mariadb
import os
import urllib3

urllib3.disable_warnings()


# Variables de entorno

#USUARIO, PASSWORD E INDICE DE ELASTICSEARCH
ELASTIC_INDEX = os.getenv("ELASTICINDEX")

#USUARIO, PASSWORD Y PUERTO DE MARIADB
MARIADB_USER = os.getenv("MARIADB_USER")
MARIADB_ENDPOINT = os.getenv("MARIADBENDPOINT")
MARIADB_PASSWORD = os.getenv("MARIADBPASS")
MARIADB_PORT = os.getenv("MARIADBPORT")
MARIADB_DB = os.getenv("MARIADB_DB")


# Inicializa el API
app = Flask(__name__)

@app.route('/app/getData')
def getMessage():

    # Conexión con MariaDB
    try:
        conn = mariadb.connect(
            user=MARIADB_USER,
            password=MARIADB_PASSWORD,
            host=MARIADB_ENDPOINT,
            port=int(MARIADB_PORT),
            database=MARIADB_DB,
        )

        cur = conn.cursor()
        cur.execute(f"INSERT INTO jobs(created_time,_status,end_time,loader,grp_size) VALUES (NOW(), 'new', NULL, NULL, 100);")

        # Código de https://stackoverflow.com/questions/43796423/python-converting-mysql-query-result-to-json
        # Convierte el resultado del select en un json
        row_headers=[x[0] for x in cur.description] #this will extract row headers
        rv = cur.fetchall()
        json_data=[]
        for result in rv:
                json_data.append(dict(zip(row_headers,result)))

        conn.close()

        return json.dumps(json_data)

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return (f"Error connecting to MariaDB Platform: {e}")

@app.route('/app/insertJob', methods=["POST"])
def insertJob():

    # Conexión con MariaDB
    try:
        conn = mariadb.connect(
            user=MARIADB_USER,
            password=MARIADB_PASSWORD,
            host=MARIADB_ENDPOINT,
            port=int(MARIADB_PORT),
            database=MARIADB_DB,
        )

        cur = conn.cursor()
        cur.execute(f"INSERT INTO jobs(created_time,_status,end_time,loader,grp_size) VALUES (NOW(), 'new', NULL, NULL, 30)")
        conn.commit()
        conn.close()

        return "Nuevo job insertado"

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return (f"Error connecting to MariaDB Platform: {e}")

# Corre el API
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

##http://127.0.0.1:5000/app/getData