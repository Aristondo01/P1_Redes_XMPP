

def get_User_Password():
    valido = False
    while not valido:
        user = input("Ingrese el nombre de usuario: ")
        password = input("Ingrese la contraseña: ")
        if user != "" and password != "":
            valido = True
        else:
            print("\033[31m\nNo se pueden dejar campos vacíos\033[37m")
    return user, password

def menu_principal():
    valido = False
    while not valido:
        print("\033[32m\nBienvenido a la aplicación de mensajería \033[0m")
        print("\033[36mLas opciones son las siguientes: ")
        print("1. Administración de usuarios")
        print("2. Comunicación")
        print("3. Salir")
        opcion = input("Ingrese la opción que desea:\033[0m")
        if opcion == "1" or opcion == "2" or opcion == "3":
            valido = True
        else:
            print("\033[31m\nOpción inválida\033[37m")
    return int(opcion)

def menu_login(primera_vez):
    valido = False
    while not valido:
        print("\033[32m\nBienvenido a la administración de usuarios \033[0m")
        print("\033[36mLas opciones son las siguientes: ")
        print("1. Registrar nueva cuenta")
        print("2. Iniciar sesión")
        print("3. Cerrar Sesión")
        print("4. Eliminar cuenta")
        if not primera_vez:
            print(". Regresar al menú principal")
        opcion = input("Ingrese la opción que desea: \033[0m")
        
        if opcion == "1" or opcion == "2" or opcion == "3" or opcion == "4" or (opcion == "5" and not primera_vez):
            valido = True
        else:
            print("\033[31m Opción inválida\033[37m")
            
    return int(opcion)
    
def menu_comunicacion():
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
        print("7. Enviar/recibir notificaciones")
        print("8. Enviar/recibir archivos")
        print("9. Regresar al menú principal")
        opcion = input("Ingrese la opción que desea: \033[0m")
        
        if opcion == "1" or opcion == "2" or opcion == "3" or opcion == "4" or opcion == "5" or opcion == "6" or opcion == "7" or opcion == "8" or opcion == "9":
            valido = True
        else:
            print("\033[31m Opción inválida\033[37m")
    
    return int(opcion)
    
    
