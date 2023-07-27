
import slixmpp
import slixmpp
import xmpp


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
    
    def __init__(self,jid,password):
        super().__init__(jid,password)
        
        