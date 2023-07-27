import text_manager as tm
import asyncio
import slixmpp
import client_manager
from client_manager import client
def menu_manager():
    primera_vez = True
    op = tm.menu_login(primera_vez)
    primera_vez = False
    
    if op == 1:
        user,password = tm.get_User_Password()
        
        if client_manager.register(user,password):
            print("Usuario registrado con éxito")
        else:
            print("No se pudo registrar el usuario")
    
    
    
    #tm.menu_comunicacion()
    




menu_manager()
    
    
    