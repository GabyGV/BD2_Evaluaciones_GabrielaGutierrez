############################################################
#    Tarea Corta 2      #    Gabriela Gutiérrez Valverde   #
#       SECAPP          #    Brayan Marín Quirós           #
#     Python API        #    David Achoy Yakimova          #
############################################################

#Importaciones
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

## circulos

## navegacion

## registro

## principal


# Conexión con firebase
cred = credentials.Certificate("firebase-sdk.json")

firebase_admin.initialize_app(cred, {

    "databaseURL": "https://secapp-db-default-rtdb.firebaseio.com/"
})

# Datos de prueba para subir
latitud = "1.51545"
longitud = "174.117"
tipoPeligro = "Intento de asalto"
fechaHora = "2022-04-22 10:34:23"
mensaje = "Tipo extraño quiere asaltar"
sennalesUbicacion = "Frente a escuela"
votos = "1"
fechaUltMod = "2022-04-22 10:34:24"


# Set se utiliza para subir datos a la base
ref = db.reference("/")
ref.set({
    "peligros": {
        "peligro":{
            "latitud": latitud,
            "longitud": longitud,
            "tipoPeligro": tipoPeligro,
            "fechaHora": fechaHora,
            "mensaje": mensaje,
            "sennalesUbicacion": sennalesUbicacion,
            "votos": votos,
            "fechaUltMod": fechaUltMod
        }
    }
})

# Get se utiliza para obtener datos desde la base
ref = db.reference("peligros")
print(ref.get())

def menu():
    print("Menú\n" 
            "1. Circulos \n",
            "2. Navegación \n",
            "3. Registro \n",
            "0. Salir\n")
    try:
        opcion = int(input("Opción: "))
        if(opcion == 0):
            return 0
        elif(opcion == 1):
            print("Llamar círculos")
        elif(opcion == 2):
            print("Llamar navegacion")
        elif(opcion == 3):
            print("Registro")
        else:
            error = int("error")
        menu()
    except:
        print("\nOpción inválida\n")
        menu()

#menu()

