import threading
import time

def mostrar_menu():
    while True:
        print("1. Opción 1")
        print("2. Opción 2")
        print("3. Opción 3")
        time.sleep(5)  # Simulamos un menú que se actualiza cada 5 segundos

def mostrar_notificaciones():
    while True:
        # Código para obtener y mostrar notificaciones en el chat
        print("Notificación: Nueva notificación importante")
        time.sleep(2)  # Simulamos una espera para obtener nuevas notificaciones

# Crear y ejecutar los hilos
hilo_menu = threading.Thread(target=mostrar_menu)
hilo_notificaciones = threading.Thread(target=mostrar_notificaciones)

hilo_menu.start()
hilo_notificaciones.start()

# Esperar a que el hilo del menú termine (esto nunca ocurrirá en este ejemplo, pero es solo para mantener el programa en ejecución)
hilo_menu.join()
