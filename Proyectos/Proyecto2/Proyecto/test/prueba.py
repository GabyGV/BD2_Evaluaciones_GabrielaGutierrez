import requests
import json
from datetime import datetime
from elasticsearch import Elasticsearch
import mariadb
import pika


try:
    URL = ("https://api.biorxiv.org/covid19/0")
    page = requests.get(URL)

    docs = json.loads(page.text)
    docs = docs['collection']

    for doc in docs: #cada doc del grupo

        
        title = doc["rel_title"]
        date = doc["rel_date"]
        rel_authors = doc["rel_authors"]
        category = doc["category"]
        rel_abs = doc["rel_abs"]
        rel_doi = doc["rel_doi"]
        rel_site = doc["rel_site"]

        jsonDoc = {} 
        jsonDoc["title"]= title
        jsonDoc["date"]= date
        jsonDoc["athors"]= rel_authors
        jsonDoc["category"]= category
        jsonDoc["abstract"]= rel_abs
        jsonDoc['rel_doi'] = rel_doi
        jsonDoc['rel_site'] = rel_site


        print("\n")
        print(jsonDoc)


        

    statusW = "completed"
except:
    mensajeError = "Error al extraer de la página"
    statusW = "error"

