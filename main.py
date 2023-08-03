import text_manager as tm
import asyncio
import slixmpp
import client_manager
from client_manager import client
from delete_client import Delete_Cliente
def menu_manager():
    
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    primera_vez = True
    #while not finish:
    op =0
    while op != 4:
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
            user= "aristondo20880"+ user + '@alumchat.xyz'
            d_client = Delete_Cliente(user,password)
            d_client.connect(disable_starttls=True)
            d_client.process(forever=False)
        elif op == 4:
            print("Gracias por usar el programa")
            
            
            
            









menu_manager()
    
    
    