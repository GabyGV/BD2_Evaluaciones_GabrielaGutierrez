#Librerias
from elasticsearch import Elasticsearch
import mariadb
import math
import os
import json

 

#Conexion con ES
client = Elasticsearch("http://localhost:59647/")
print(client.indices.exists(index="jobs"))


#Verificar Indices Jobs y Group
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



#Parametros de busca
search_param = {

    "terms": {
        "status": [ "new" ]
    }
    
}
while True:

    try:
        response = client.search(index="jobs", query=search_param)
    #print(response["hits"]["hits"][0]["_source"]["source"])
        hitsJson = response["hits"]["hits"][0]
        id = hitsJson["_id"]
        _sourceJson = response["hits"]["hits"][0]["_source"]
    
        job_id = _sourceJson["job_id"]
        print(job_id)
        sourceJson = response["hits"]["hits"][0]["_source"]["source"]
        data_sources = response["hits"]["hits"][0]["_source"]["data_sources"]
        expression = sourceJson['expression']
        gpr_size = int(sourceJson['grp_size'])
        data_source = sourceJson['data_source']
        for x in data_sources:
            if x["name"] == data_source:
                print(x)
        body = {
        "doc":{
        "status" : "inprogress"}}

        #updateComp = client.update(index='jobs',doc_type="_doc",id=id, body=body)
        #print ('response:', updateComp)
        
        print(expression)
        print(gpr_size)
        print(data_source)

        try:
            conn = mariadb.connect(
            user="root",
            password="l9mXQYS6eL",
            host="127.0.0.1",
            port=50908,
            database="people_db"
        )
            cur = conn.cursor()
            cur.execute(f"SELECT COUNT(1) FROM ({expression}) AS a")
            total= cur.fetchone()
            print(int(total[0]))
            totalDocs =math.ceil(total[0]/gpr_size)
            initialValue = 0

            for x in range(totalDocs):
                newGroup = {
                    "job_id": f"{job_id}",
                    "group_id":  f"{job_id}-{initialValue}"
                }
                add = client.index(index="groups",doc_type='_doc', document=newGroup)
                initialValue += gpr_size
                print(newGroup)

            
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
        

    except:
        print("No hay documentos para processar")  






























#1000 elementos / 100 = 10
#0 hasta 99 
#100 hasta 199
#...
#job606-0
#job606-100

'''
response = response["hits"]["hits"]
response = json.dumps(response[0])
y = json.loads(response)

'''

##Conectar con MAriaDB
##enviar el archivo a rabbit
##update del doc


'''
#Parte de MariaDB
def get_field_info(cur):
    field_info = mariadb.fieldinfo()
    field_info_text = []
    for column in cur.description:
      column_name = column[0]
      column_type = field_info.type(column)
      column_flags = field_info.flag(column)

      field_info_text.append(f"{column_name}: {column_type} {column_flags}")

    return field_info_text

try:
    conn = mariadb.connect(
        user="root",
        password="l9mXQYS6eL",
        host="127.0.0.1",
        port=50908,
        database="people_db"
    )
    cur = conn.cursor()
    cur.execute("SELECT Cedula FROM Person")
    row= cur.fetchall()
    print(*row) 
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    
'''
# Get Cursor




####
#Listo el update


####
#falta el total de registros a migrar