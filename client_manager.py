
import slixmpp
import xmpp
from slixmpp.exceptions import IqError, IqTimeout
import text_manager as tm
import asyncio
from aioconsole import ainput
from aioconsole.stream import aprint
import threading

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
        self.name_domain = user
        self.is_connected = False    
        
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # Ping
        self.register_plugin('xep_0045') # MUC
        self.register_plugin('xep_0085') # Notifications
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0060') # PubSub


        # Chat GPT explico como funcionan los manejadores de eventos
        self.add_event_handler("session_start", self.LogIn)
        self.add_event_handler('subscription_request', self.suscripcion_entrante)
        
        
    
    
    async def LogIn(self,event):
        
        try :
            self.send_presence()
            await self.get_roster()
            self.is_connected = True
            print("\033[32mInicio de sesión exitoso\033[0m")
            
            asyncio.create_task(self.async_menu())
            #asyncio.create_task(self.thread_init())
            
            
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
    
    
    async def estado_contactos(self):
        # Sugerencia de Copilot
        #-------------------------
        roster = self.client_roster
        concats = roster.keys()
        concats = [jid for jid in roster.keys() if jid != self.name_domain]

        #-------------------------
        
        Lista_contactos = []
        
        if not concats:
            print("\033[38;5;208mLista de contactos vacía\033[0m")
            return
            
        for u in concats:
            conn = roster.presence(u)
            show = '\033[92mDisponible \033[0m'
            status = ''
            
            for answer, pres in conn.items():
                if pres['show']:
                    show = pres['show']
                status = pres['status']
                
                if show == 'dnd':
                    show = '\033[31mOcupado\033[0m'
                if show == 'xa':
                    show = '\033[31mNo disponible\033[0m'
                if show == 'away':
                    show = '\033[38;5;208mAusente\033[0m'
            
            Lista_contactos.append((u,show,status))
        print('\n\033[92mLista de contactos:\033[0m')
        for i in range(len(Lista_contactos)):
            print('\033[38;5;208m',i+1,')\033[96m',end =" ")
            print('Contacto: ',Lista_contactos[i][0],end =" ---> ")
            print('Estado:',Lista_contactos[i][1],'\033[96m Mensaje:',Lista_contactos[i][2])
        print('\n')
        
        
    async def agregar_contacto(self):
        user_add = input("Ingresa el nombre del usuario que deseas agregar (sin @alumchat.xyz): ")+ '@alumchat.xyz'
        
        try:
            self.send_presence_subscription(pto = user_add)
            print("Se ha enviado una solicitud de suscripción a:", user_add)
            await self.get_roster()
        except IqError as e:
            print(f"\033[Problemas para enviar la solicitud: {e.iq['error']['text']}\033[0m")
        except IqTimeout:
            print("\033[31mError:\nSe ha excedido el tiempo de respuesta\033[0m")
    
    async def suscripcion_entrante(self,presence):
        print(f"Recibida solicitud de suscripción de {presence['from']}")
        if presence['type'] == 'subscribe':
            # Automatically accept the subscription request
            try:
                self.send_presence_subscription(pto=presence['from'], ptype='subscribed')
                await self.get_roster()
                print(f"Accepted subscription request from {presence['from']}")
            except IqError as e:
                print(f"Error accepting subscription request: {e.iq['error']['text']}")
            except IqTimeout:
                print("No response from server.")
                
    async def thread_init(self):
        hilo1 = threading.Thread(target=self.async_menu)
        hilo1.start()
        hilo1.join()
        
    async def async_menu(self):
        
        while self.is_connected:
            op = await tm.menu_comunicacion()
            
            if op == 1:
                await self.estado_contactos()
            if op == 2:
                await self.agregar_contacto()
            
            
        
        
        
        
        