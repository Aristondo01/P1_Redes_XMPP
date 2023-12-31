from aioconsole import ainput
from aioconsole.stream import aprint


"""
Este archivo tiene como objetivo manejar la mayoria de inputs y menus para mostrar en la CLI
"""

# Obtiene el nombre de usuario y la contraseña del usuario
def get_User_Password(accion):
    valido = False
    while not valido:
        print("\033[32m"+accion)
        user = input("Ingrese el nombre de usuario: \033[0m")
        password = input("\033[32mIngrese la contraseña: \033[0m")
        if user != "" and password != "":
            valido = True
        else:
            print("\033[31m\nNo se pueden dejar campos vacíos\033[37m")
    return user, password

# Menu principal para iniciar sesion o registrarse
def menu_login(primera_vez):
    valido = False
    while not valido:
        print("\033[32m\nBienvenido a la administración de usuarios \033[0m")
        print("\033[36mLas opciones son las siguientes: ")
        print("1. Registrar nueva cuenta")
        print("2. Iniciar sesión")
        print("3. Eliminar cuenta")
        if not primera_vez:
            print("4. Cerrar programa")
        opcion = input("Ingrese la opción que desea: \033[0m")
        
        if opcion == "1" or opcion == "2" or opcion == "3" or (opcion == "4" and not primera_vez):
            valido = True
        else:
            print("\033[31m Opción inválida\033[37m")
            
    return int(opcion)

#Menu interno para el cliente de slixmpp   
async def menu_comunicacion():
    valido = False
    while not valido:
        print("\033[32m\nBienvenido a la comunicación \033[0m")
        print("\033[36mLas opciones son las siguientes: ")
        print("1. Mostrar todos los contactos y su estado")
        print("2. Agregar un usuario a los contactos")
        print("3. Mostrar detalles de contacto de un usuario")
        print("4. Comunicación 1 a 1 con cualquier usuario/contacto")
        print("5. Participar en conversaciones grupales")
        print("6. Definir mensaje de presencia")
        print("7. Enviar archivos")
        print("8. Cerrar sesión")
        opcion = await ainput("Ingrese la opción que desea: \033[0m")
        
        if opcion == "1" or opcion == "2" or opcion == "3" or opcion == "4" or opcion == "5" or opcion == "6" or opcion == "7" or opcion == "8" :
            valido = True
        else:
            print("\033[31m Opción inválida\033[37m")
    
    return int(opcion)
    
    
