
#Librerias
import mariadb
import time

#Variables de entorno
#Conexion con ES
while True:
    print("hola")
    try:
        conn = mariadb.connect(
        user="root",
        password = "R1NE0s45L1",
        host="databases-mariadb-primary",
        port=3306,
        database= "people_db"
    )
        print("Se conecto con mariaDB")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")

    time.sleep(8)













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