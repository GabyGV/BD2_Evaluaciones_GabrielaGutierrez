import names

MARIADB_ENDPOINT = "MARIADBENDPOINT"
MARIADB_PASSWORD = "MARIADBPASS"
MARIADB_PORT = "MARIADBPORT"

def cargarDatos():
    conn = mariadb.connect(
        user="root",
        password=MARIADB_PASSWORD,
        host=MARIADB_ENDPOINT,
        port=3306,
        database=data_source,
    )
    cur = conn.cursor()

cant = 500

while (cant != 0):
    print(names.get_full_name())
    cant -= 1