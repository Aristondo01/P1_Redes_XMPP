import text_manager as tm
import asyncio
import slixmpp


def menu_manager():
    primera_vez = True
    tm.menu_login(primera_vez)
    primera_vez = False
    
    
    tm.menu_comunicacion()




menu_manager()
    
    
    