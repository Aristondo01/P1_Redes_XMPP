import text_manager as tm
import asyncio
import slixmpp
import client_manager
from client_manager import client
def menu_manager():
    
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    log_in = False
    primera_vez = True
    finish = False
    #while not finish:
    op = tm.menu_login(primera_vez)
    primera_vez = False
    
    if op == 1:
        user,password = tm.get_User_Password("Ingrese los datos a registrar")
        
        if client_manager.register(user,password):
            print("Usuario registrado con éxito")
        else:
            print("No se pudo registrar el usuario")
        
    elif op == 2:
        user,password = tm.get_User_Password("Ingrese los datos a iniciar sesión")
        user= "aristondo20880"+ user + '@alumchat.xyz'
        cliente = client(user,password)
        # Sugerencia de Copilot
        #----------------
        cliente.connect(disable_starttls=True)
        cliente.process(forever=False)
        #----------------
    
    elif op == 3:
        user,password = tm.get_User_Password("Ingrese los datos para borrar su cuenta")
        
        
        









menu_manager()
    
    
    