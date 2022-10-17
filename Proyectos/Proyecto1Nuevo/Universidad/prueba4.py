
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



conn = mariadb.connect(
    user="root",
    password="08eR8ksufp",
    host="localhost",
    port=50908,
    database="people_db",
)

cur = conn.cursor()
cur.execute(f"SELECT * FROM persona ORDER BY cedula LIMIT 0, 100")
#linea de codigo sacada de 
#https://stackoverflow.com/questions/5010042/mysql-get-column-name-or-alias-from-query
#para transformar tabblas de mariadb a una lista de jsons
res = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
for x in res:
    print(x)