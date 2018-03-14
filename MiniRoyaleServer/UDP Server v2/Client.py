import threading
import socket

clients_lock = threading.Lock()
clients = {}


class Client:
    
    def __init__(self, addr):
        print("init")
        self.addr = addr
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()
        
    def run(self):
        print("creating socket")
        #Binded Ip
        self.server_ip = "0.0.0.0"
        #Random available Port
        self.server_port = 0 #random 
        #One socket for each client
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #internet, UDP
        #Bind socket and generate a new open port
        self.socket.bind((self.server_ip, self.server_port))
        #Store generated port
        self.server_port = self.socket.getsockname()[1] #new port
        #Send newly generated socket info to client
        self.send("PORT:"+str(self.server_port)+";");
        #Listen to the port
        while True:        
            #Receive
            data, addr = self.socket.recvfrom(1024) # buffer size is 1024 bytes
            text = data.decode('utf-8') #Decode message
            self.msg_received(text) #Message Received
            
    
    def send(self,text):
        print("sending:"+text)
        self.socket.sendto(bytes(text, 'utf-8'),self.addr)
        
    
    def msg_received(self,text):
        print("received:"+text)





  


def new_connection(addr):
    
    with clients_lock:
        if not addr in clients:
            print("new connection will commence")
            c = Client(addr)
            clients[addr] = c
        else:
            print("no new connection")
    
    print("tried to connect")