
import slixmpp
import xmpp
from slixmpp.exceptions import IqError, IqTimeout
import text_manager as tm
from aioconsole import ainput
import asyncio
from asyncio import Future


def register(client, password):

    client ="aristondo20880"+ client + '@alumchat.xyz'
    jid = xmpp.JID(client)
    account = xmpp.Client(jid.getDomain(), debug=[])
    account.connect()
    return bool(
	    xmpp.features.register(account, jid.getDomain(), {
	        'username': jid.getNode(),
	        'password': password
	    }))  


class client(slixmpp.ClientXMPP):
    
    def __init__(self,user,password):
        super().__init__(user,password)
        self.name = user.split('@')[0]
        self.is_connected = False
        
        
        
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # Ping
        self.register_plugin('xep_0045') # MUC
        self.register_plugin('xep_0085') # Notifications
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0060') # PubSub


        
        
        # Chat GPT explico como funcionan los manejadores de eventos
        self.add_event_handler("session_start", self.LogIn)
        
    
    async def LogIn(self,event):
        
        try :
            self.send_presence()
            await self.get_roster()
            self.is_connected = True
            print("\033[32mInicio de sesión exitoso\033[0m")
            
            asyncio.create_task(self.async_menu())
            
        except IqError as errorIE:
            print("\033[31mError:\nNo se pudo iniciar sesión\033[0m")
            self.is_connected = False
            self.disconnect()
        except IqTimeout:
            print("\033[31mError:\nSe ha excedido el tiempo de respuesta\033[0m")
            self.is_connected = False
            self.disconnect()
        
        except Exception as e:
            print("\033[31mError:\n",e,"\033[0m")
            self.is_connected = False
            self.disconnect()
            
    
    async def async_menu(self):
        
        while self.is_connected:
            tm.menu_comunicacion()
            op = await ainput ("\033[36mIngrese la opción que desea: \033[0m")
            print("La opción ingresada es: ",op)
            
        
        
        
        
        