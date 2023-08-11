
import slixmpp
import xmpp
from slixmpp.exceptions import IqError, IqTimeout
import text_manager as tm
import asyncio
from aioconsole import ainput
from aioconsole.stream import aprint
import threading
import time
import random

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
        self.notificacion = []
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
        self.add_event_handler("message", self.message)
        self.add_event_handler("groupchat_invite", self.auto_accept_invite)
        
        
    async def auto_accept_invite(self, inv):
        groupchat_jid = inv["from"]
        await aprint(f"\033[38;2;0;255;255m\nNotificación: Se ha unido al grupo {groupchat_jid} \033[0m")
        self.plugin['xep_0045'].join_muc(groupchat_jid, self.boundjid.user)
        self.send_presence(pto=groupchat_jid, ptype="available")       
        
    async def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            await aprint(f"\033[38;2;0;255;255m\nNotificación: Mensaje recibido de {msg['from']}: \nMensaje: {msg['body']}\n \033[0m")
        if msg['type'] == ('groupchat'):
            msg_string = str(msg['from'])
            grup = msg_string.split("@")[0]
            de = msg_string.split("/")[1]
            if de != self.name:
                await aprint(f"\033[38;2;0;255;255m\nNotificación: Mensaje recibido de {de} en el grupo {grup}: \nMensaje: {msg['body']}\n \033[0m")
    
    async def LogIn(self,event):
        
        try :
            self.send_presence()
            await self.get_roster()
            self.is_connected = True
            print("\033[32mInicio de sesión exitoso\033[0m")
            roster = self.client_roster
            self.amigos = [jid for jid in roster.keys() if jid != self.name_domain]            
            self.conexiones = await self.get_contacts()
           
            self.amistad = asyncio.create_task(self.notif_amistad())
            self.notif = asyncio.create_task(self.notif_conectado())
            self.menu = asyncio.create_task(self.async_menu())
            
            
            
        except IqError as errorIE:
            print("\033[31m\nError:\nNo se pudo iniciar sesión\033[0m")
            self.is_connected = False
            self.disconnect()
        except IqTimeout:
            print("\033[31m\nError:\nSe ha excedido el tiempo de respuesta\033[0m")
            self.is_connected = False
            self.disconnect()
        
        except Exception as e:
            print("\033[31m\nError:\n",e,"\033[0m")
            self.is_connected = False
            self.disconnect()
            
    async def get_contacts(self):
        await self.get_roster()
        roster = self.client_roster
        concats = roster.keys()
        concats = [jid for jid in roster.keys() if jid != self.name_domain]

        
        Lista_contactos = {}
        
        if not concats:
            return Lista_contactos
            
        for u in concats:
            conn = roster.presence(u)
            show = 'NC'
            
            for answer, pres in conn.items():
                show,status = await self.estado_mensaje(pres)
                
                if show == '\033[92mDisponible\033[0m':
                    show = "YC"
                else:
                    show = "NC"
                
            if "@conference.alumchat.xyz" not in u:
                Lista_contactos[u] = show
            
        return Lista_contactos
            
    
    async def notif_conectado(self):
        while True:
            try:
                await asyncio.sleep(0.1)
                compare = await self.get_contacts()
                
                for key in self.conexiones.keys():
                    if key in compare.keys():
                        if self.conexiones[key] != compare[key]:
                            if self.conexiones[key] == "NC" and compare[key] == "YC":
                                await aprint("\033[38;2;0;255;255m\nNotificación: "+key.split("@")[0]+" acaba de cambiar su estado a disponible\033[0m\n")            
                            if self.conexiones[key] == "YC" and compare[key] == "NC":
                                await aprint("\033[38;2;0;255;255m\nNotificación: "+key.split("@")[0]+" se acaba de desconectar\033[0m\n")            
                                
                
                self.conexiones = compare.copy()
                time.sleep(2.5)
            except IqTimeout:
                print("\033[31m\nError:\nTu conexión con el servidor es mala\033[0m")
            
    
    async def notif_amistad(self):
        while True:
            try:
                await asyncio.sleep(0.1)
                #if random.randint(0,3) == 2:
                #    await aprint("\033[38;2;0;255;255m\n"+"Notificacion falsa"+"\n\033[32m")
                
                await self.get_roster()
                roster = self.client_roster
                concats = [jid for jid in roster.keys() if jid != self.name_domain]
                if concats == self.amigos:
                    continue
                else:
                    for jid in concats:
                        if jid not in self.amigos and "conference.alumchat.xyz" not in jid:
                            await aprint("\033[38;2;0;255;255m\nNotificación: Se ha agregado a",jid.split("@")[0],"\033[0m\n")
                            self.amigos.append(jid)
                    self.amigos = concats.copy()
                    
                time.sleep(2.5)
            except IqTimeout:
                print("\033[31m\nError:\nTu conexión con el servidor es mala\033[0m")
            
    async def signal_handler(self,signal,frame):
        self.disconnect()
            
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
    
    
    async def estado_mensaje(self,pres):
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
            
        return show,status
        
    
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
            status = '\033[90mNo visible \033[0m'
            
            for answer, pres in conn.items():
                show,status = await self.estado_mensaje(pres)
                
            if "conference.alumchat.xyz" not  in u:
                Lista_contactos.append((u,show,status))
        print('\n\033[92mLista de contactos:\033[0m')
        for i in range(len(Lista_contactos)):
            print('\033[38;5;208m',i+1,')\033[96m',end =" ")
            print('Contacto: ',Lista_contactos[i][0],end =" ---> ")
            print('Estado:',Lista_contactos[i][1],'\033[96m Mensaje:',Lista_contactos[i][2])
        print('\n')
        
        
    async def agregar_contacto(self):
        user_add = input("\033[96mIngresa el nombre del usuario que deseas agregar (sin @alumchat.xyz): \033[0m")+ '@alumchat.xyz'
        
        try:
            self.send_presence_subscription(pto = user_add)
            print("\033[96mSe ha enviado una solicitud de suscripción a:", user_add)
            await self.get_roster()
        except IqError as e:
            print(f"\033[31m\nProblemas para enviar la solicitud: {e.iq['error']['text']}\033[0m")
        except IqTimeout:
            print("\033[31m\nError:\nSe ha excedido el tiempo de respuesta\033[0m")
            
    async def change_user(self,name):
        self.notificacion.append(name)
    
    async def suscripcion_entrante(self,presence):
        if presence['type'] == 'subscribe':
            # Automatically accept the subscription request
            try:
                self.send_presence_subscription(pto=presence['from'], ptype='subscribed')
                await self.get_roster()
                await self.change_user(presence['from'])
                await aprint(f"Accepted subscription request from {presence['from']}")
            except IqError as e:
                print(f"\033[Problemas para enviar la solicitud: {e.iq['error']['text']}\033[0m")
            except IqTimeout:
                print("\033[31m\nError:\nSe ha excedido el tiempo de respuesta\033[0m")
                
    async def contaco_specifico(self):
        contacto = input("\033[36mIngresa el nombre del contacto que deseas consultar (sin @alumchat.xyz): \033[0m")
        contacto+='@alumchat.xyz'
        roster = self.client_roster
        contactos = roster.keys()
        
        if contacto not in contactos:
            print("\033[31mEl contacto no esta en tu lista :(\033[0m")
        else:
            conn = roster.presence(contacto)
            show = '\033[90mDesconectado \033[0m'
            status = '\033[90mNo visible \033[0m'
            
            for answer, pres in conn.items():
                show,status = await self.estado_mensaje(pres)
                
                
            print('\033[38;5;208mContacto solicitado: \033[96m',contacto,end =" ---> ")
            print('Estado:',show,'\033[96m Mensaje:',status)
            
            
    async def menu_mensajes_priv(self):
        enviar_a = await self.get_contacts()
        await aprint('\033[92mLista de contactos:\033[0m')
        cont=1
        dicct = {}
        for key in enviar_a.keys():
            if "conference.alumchat.xyz" not  in key:
                await aprint('\033[38;5;208m',cont,')\033[96m',key)
                dicct[cont] = key
                cont+=1
            
        valido = False
        
        while not valido:
            try:
                op = await ainput("\033[96mIngresa el número del contacto al que deseas enviar un mensaje: \033[0m")
                op = int(op)
                if op > 0 and op <= len(enviar_a):
                    valido = True
                else:
                    await aprint("\033[31mIngresa un número válido\033[0m")
            except ValueError:
                await aprint("\033[31mIngresa un número válido\033[0m")
        
        try: 
            men = await ainput("\033[96mIngresa el mensaje que deseas enviar: \033[0m")
            self.send_message(mto = dicct[op], mbody=men,mtype='chat')
            await aprint("\033[92mMensaje enviado\033[0m")
        except IqError as e:
            await aprint(f"\033[Problemas para enviar la solicitud: {e.iq['error']['text']}\033[0m")

    async def group_chat_menu(self):
        salir = False
        
        while not salir:
            await aprint("\033[92mBienvenido al menu de chat grupal elige una opción\033[0m")
            await aprint("\033[38;5;208m1)\033[96m Crear sala\033[0m")
            await aprint("\033[38;5;208m2)\033[96m Unirse a sala\033[0m")
            await aprint("\033[38;5;208m3)\033[96m Enviar mensaje\033[0m")
            await aprint("\033[38;5;208m4)\033[96m Invitar a sala\033[0m")
            await aprint("\033[38;5;208m5)\033[96m Regresar al menu principal\033[0m")
            
            valido = False
            
            while not valido:
                try:
                    op = await ainput("\033[96mIngresa el número de la opción que deseas: \033[0m")
                    op = int(op)
                    if op > 0 and op <= 5:
                        valido = True
                    else:
                        await aprint("\033[31mIngresa un número válido\033[0m")
                except ValueError:
                    await aprint("\033[31mIngresa un número válido\033[0m")
            if op == 1:
                try:
                    room = await ainput("\033[96mIngresa el nombre de la sala a crear: \033[0m")
                    room += '@conference.alumchat.xyz'
                    await self.plugin['xep_0045'].join_muc(room, self.boundjid.user)
                    await asyncio.sleep(1)
                    
                    form = self.plugin['xep_0004'].make_form(ftype='submit', title='Config')

                    form['muc#roomconfig_roomname'] = room
                    form['muc#roomconfig_persistentroom'] = '1'
                    form['muc#roomconfig_publicroom'] = '1'
                    form['muc#roomconfig_membersonly'] = '0'
                    form['muc#roomconfig_allowinvites'] = '1'
                    form['muc#roomconfig_enablelogging'] = '1'
                    form['muc#roomconfig_changesubject'] = '1'
                    form['muc#roomconfig_maxusers'] = '100'
                    form['muc#roomconfig_whois'] = 'anyone'
                    form['muc#roomconfig_roomdesc'] = 'Chat_grupal'
                    form['muc#roomconfig_roomowners'] = [self.name_domain]
                    await self.plugin['xep_0045'].set_room_config(room, config=form)
                    self.send_message(mto=room, mbody="Sala de chat creada", mtype='groupchat')
                    
                    await aprint("\033[92mSala creada exitosamente\033[0m")
                except IqError as e:
                    await aprint(f"\033[31mProblemas para enviar la solicitud: {e.iq['error']['text']}\033[0m")
                except IqTimeout:
                    await aprint("\033[31mNo se pudo conectar con el servidor\033[0m")
                
            elif op == 2:
                try:
                    room = await ainput("\033[96mIngresa el nombre de la sala a la que deseas unirte: \033[0m")
                    room += '@conference.alumchat.xyz'
                    
                    
                    self.plugin['xep_0045'].join_muc(room, self.boundjid.user)
                    await aprint("\033[92mTe has unido a la sala exitosamente\033[0m")
                    
                            
                            
                except IqError as e:
                    await aprint(f"\033[Problemas para enviar la solicitud: {e.iq['error']['text']}\033[0m")
                except IqTimeout:
                    await aprint("\033[31mNo se pudo conectar con el servidor\033[0m")
                    
            elif op == 3:
                grup =  await ainput("\033[96mIngresa el nombre del grupo: \033[0m")
                grup += "@conference.alumchat.xyz"
                men = await ainput("\033[96mIngresa el mensaje que deseas enviar: \033[0m")
                
                try:
                    self.send_message(mto = grup, mbody=men,mtype='groupchat')
                except IqTimeout:
                    print("\033[31m\nError:\nTu conexión con el servidor es mala\033[0m")
                except IqError:
                    print("\033[31m]No se pudo enviar el mensaje")
                
            elif op == 4:
                try:
                    room = await ainput("\033[96mIngresa el nombre del chat grupal:  \033[0m")
                    user = await ainput("\033[96mIngresa el nombre del usuario a invitar (sin @alumchat.xyz): \033[0m")
                    user += '@alumchat.xyz'
                    self.plugin['xep_0045'].invite(
                        room = room+"@conference.alumchat.xyz",
                        jid = user,
                        reason = "Join the new group chat"
                    )
                    
                except IqError as e:
                    await aprint(f"\033[Problemas para enviar la solicitud: {e.iq['error']['text']}\033[0m")
                except IqTimeout:
                    await aprint("\033[31mNo se pudo conectar con el servidor\033[0m")
            
            elif op == 5:
                salir = True


        
        
        
        
    async def async_menu(self):
        
        while self.is_connected:
            op = await tm.menu_comunicacion()
            
            if op == 1:
                await self.estado_contactos()
            if op == 2:
                await self.agregar_contacto()
            if op == 3:
                await self.contaco_specifico()
            if op == 4:
                await self.menu_mensajes_priv()
            if op == 5:
                await self.group_chat_menu()
            if op == 6:
                await self.cambiar_mensaje_estado()
            if op == 7:
                pass
            if op == 8:
                print("\033[31mCerrando sesión...\033[0m")
                self.disconnect()
                self.is_connected = False
                self.menu.cancel()
                self.notif.cancel()
                self.menu.cancel()
                
            
            
        
        
        
        
        