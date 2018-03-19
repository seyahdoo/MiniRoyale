import threading
import socket
import time

from request_dispatcher import RequestDispatcher
from player import Player
import game

ping_lock = threading.Lock()
clients_lock = threading.Lock()
clients = {}


class Client:
    
    def __init__(self, addr):
        
        print("Client Init")
        
        # Client Address
        self.addr = addr
        
        # create main client thread
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()
        
    def run(self):
        print("creating socket")
        # Binded Ip
        self.server_ip = "0.0.0.0"
        # Random available Port
        self.server_port = 0 #random TODO: write zero here
        # One socket for each client
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #internet, UDP
        # Bind socket and generate a new open port
        self.socket.bind((self.server_ip, self.server_port))
        # Store generated port
        self.server_port = self.socket.getsockname()[1] #new port
        
        # listen with a new thread
        self.listener_thread = threading.Thread(target=self.listener)
        self.listener_thread.daemon = True
        self.listener_thread.start()
        
        #print("Before sending port")
        
        # Send newly generated socket info to client
        self.send("PORTO:"+str(self.server_port)+";");
        print("PORTO:"+str(self.server_port)+";")
        # create or login a player
        self.player = Player()
        print("created Player for Client, player_id:{}".format(self.player.player_id))
        
        
        # create a new thread ping 
        self.ping_thread = threading.Thread(target=self.ping_routine)
        self.ping_thread.daemon = True
        self.ping_thread.start()
        
        # send player game info
        
        antitickrate = 1/game.game_instance.tickrate
        
        while True:
            
            self.player.GetInfo(self)
            
            time.sleep(antitickrate)
        
        
            
    def listener(self):
        # Listen to the port
        while True:   
            # Receive
            data, addr = self.socket.recvfrom(1024)       
            # Decode message
            text = data.decode('utf-8') 
            # Message Received
            self.msg_received(text) 
    
    def ping_routine(self):
        # Send ping request every 1 seconds
        # Disconnect if no answer has came for 60 seconds
        while True:
            if self.player.dropout_time < 10:
                text = "PINGO;"
                #print("sending ping request, player_id:{}".format(self.player.player_id))
                self.send(text)
                with ping_lock:
                    self.player.dropout_time += 1
                time.sleep(1)
            else:
                print("Client with player_id:{} has not responded to PINGO for {} seconds.".format(self.player.player_id,self.player.dropout_time))
                return
    
    def send(self,text):
        #print("sending:"+text)
        self.socket.sendto(bytes(text, 'utf-8'),self.addr)
        
    
    # dispatch incoming player commands
    def msg_received(self,text):
        #print("UDP: received:"+text)
        RequestDispatcher(self,text)
        #commands = text.split(';')
        
        #for cmd in commands:
          #  if(cmd[0:5] == "MOVER"):
          #      args = cmd[6:]
           #     args = args.split(',')
                
                #print(str(args))
                
                # if last packet number is > args[0] return
            #    self.player.Move(args[0],args[1],args[2])
                
        
        


  


def new_connection(addr):
    
    with clients_lock:
        if not addr in clients:
            print("new connection will commence")
            c = Client(addr)
            clients[addr] = c
        else:
            print("no new connection")
    