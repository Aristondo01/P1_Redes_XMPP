
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
    
    def print_async(self, text):
        print("\033[38;2;0;255;255m"+text+"\033[0m")
            
    async def cambiar_mensaje_estado(self):
        mensaje = input("\033[32mIngresa el mensaje de estado: \033[0m")
        print("\033[32mQue status desea colocar?")
        valid = False
        while not valid:
            print('\033[31m1.Ocupado\033[0m')
            print('\033[31m2.No disponible\033[0m')
            print('\033[38;5;208m3.Ausente\033[0m')
            print('\033[92m4.Disponible\033[0m')
            inp = input("\033[32mIngresa el número de la opción: \033[0m")
            
            if inp == "1" or inp == "2" or inp == "3" or inp == "4":
                valid = True
        pshow_i= ""
        if inp == "1":
            pshow_i = "dnd"
        elif inp == "2":
            pshow_i = "xa"
        elif inp == "3":
            pshow_i = "away"
        elif inp == "4":
            pshow_i = ""
            
             
        self.send_presence(pshow = pshow_i, pstatus = mensaje)
        print("\033[32mMensaje de estado cambiado con éxito\033[0m")
    
    
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
            show = '\033[90mDesconectado \033[0m'
            status = ''
            
            for answer, pres in conn.items():
                if pres:
                    pres_show = pres['show']
                
                status = pres['status']
                
                if pres_show == 'dnd':
                    show = '\033[31mOcupado\033[0m'
                if pres_show == 'xa':
                    show = '\033[31mNo disponible\033[0m'
                if pres_show == 'away':
                    show = '\033[38;5;208mAusente\033[0m'
                if pres_show == '':
                    show = '\033[92mDisponible\033[0m'
                
                
            
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
            if op == 3:
                pass
            if op == 4:
                pass
            if op == 5:
                pass
            if op == 6:
                await self.cambiar_mensaje_estado()
                
            
            
        
        
        
        
        