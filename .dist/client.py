
import slixmpp


class client(slixmpp.ClientXMPP):
    
    def __init__(self,jid,password):
        super().__init__(jid,password)
        
        