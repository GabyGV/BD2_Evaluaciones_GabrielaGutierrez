############################################################
#    Tarea Corta 2      #    Gabriela Gutiérrez Valverde   #
#       SECAPP          #    Brayan Marín Quirós           #
#     Python API        #    David Achoy Yakimova          #
############################################################

#Importaciones
import firebase_admin

## circulos

## navegacion

## principal

def menu():
    print("Menú\n" 
            "1. Circulos \n",
            "2. Navegación \n",
            "0. Salir\n")
    try:
        opcion = int(input("Opción: "))
        if(opcion == 0):
            return 0
        elif(opcion == 1):
            print("Llamar círculos")
        elif(opcion == 2):
            print("Llamar navegacion")
        else:
            error = int("error")
        menu()
    except:
        print("\nOpción inválida\n")
        menu()

menu()