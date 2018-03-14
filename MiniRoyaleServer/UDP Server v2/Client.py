
clients = {}

class Client:
    
    
    def __init__(addr):
        print("init")
        
    
    
    
        


def new_connection(addr):
    if not addr in clients:
        print("new connection will commence")
        c = Client(addr)
        clients[addr] = c
    else:
        print("no new connection")
    
    print("tried to connect")