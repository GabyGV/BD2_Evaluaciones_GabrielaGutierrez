from elasticsearch import Elasticsearch
import mariadb
import math
import os
import json
import time
import pika
import urllib3
urllib3.disable_warnings()


#Variables de entorno

#Conexion con ES
client = Elasticsearch("https://localhost:60577/",
        http_auth=("elastic","272x3wsujB0YX5T01WE70LDt"),
        verify_certs = False)


#Verificar Indices Jobs y Group--------------------------------------------
if client.indices.exists(index="jobs") != True:
    client.indices.create(index="jobs")
    print("No existe /jobs")
else:
    print("Si existe /jobs")

if client.indices.exists(index="groups") != True:
    client.indices.create(index="groups")
    print("No existe /groups")

else:
    print("Si existe /groups")



#Parametros de busca-------------------------------------------

print("conexion con elastic")

search_param = {"terms": {"status": ["inprogress"]}}
print("conexion con elastic")

response = client.search(index="jobs", query=search_param)
# Verifica que hayan documentos con el status "new"
hitsJson = response["hits"]["hits"][0]
id = hitsJson["_id"]
_sourceJson = response["hits"]["hits"][0]["_source"]
job_id = _sourceJson["job_id"]
sourceJson = response["hits"]["hits"][0]["_source"]["source"]
data_sources = response["hits"]["hits"][0]["_source"]["data_sources"]
expression = sourceJson["expression"]
gpr_size = int(sourceJson["grp_size"])
data_source = sourceJson["data_source"]
stages = _sourceJson["stages"][0]

print(stages)