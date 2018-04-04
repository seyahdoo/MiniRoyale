import threading
import socket
import time

from request_dispatcher import request_dispatcher
from player import Player
import game

ping_lock = threading.Lock()


class Client:
    
    def __init__(self, address):
        print("Client Init")
        
        # Client Address
        self.address = address
        self.server_ip = None
        self.server_port = None
        self.socket = None

        # create main client thread
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

        self.listener_thread = None
        self.sent_packet_id = 0

        self.player = None

        self.ping_thread = None

    def run(self):
        print("creating socket")
        # Binding of Ip
        self.server_ip = "0.0.0.0"
        # Random available Port
        self.server_port = 0  # random write zero here
        # One socket for each client
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # internet, UDP
        # Bind socket and generate a new open port
        self.socket.bind((self.server_ip, self.server_port))
        # Store generated port
        self.server_port = self.socket.getsockname()[1]  # new port
        
        # listen with a new thread
        self.listener_thread = threading.Thread(target=self.listener)
        self.listener_thread.daemon = True
        self.listener_thread.start()
        # print("Before sending port")
        
        # Send newly generated socket info to client
        self.send("PORTO:"+str(self.server_port)+";")
        print("PORTO:"+str(self.server_port)+";")
        # create or login a player
        self.player = Player()
        print("created Player for Client, player_id:{}".format(self.player.player_id))
        
        # Add created player to player_list
        game.game_instance.players[self.player.player_id] = self.player
        
        # create a new thread ping 
        self.ping_thread = threading.Thread(target=self.ping_routine)
        self.ping_thread.daemon = True
        self.ping_thread.start()

        # TODO send spawned item information to player
        # self.spawnedItemInformation()

    def listener(self):
        # Listen to the port
        while True:   
            # Receive
            data, address = self.socket.recvfrom(1024)
            # Decode message
            text = data.decode('utf-8') 
            # Message Received
            self.msg_received(text) 
    
    def ping_routine(self):
        # Send ping request every 1 seconds
        # Disconnect if no answer has came for 60 seconds
        # Close main thread and delete player information in players dictionary
        dropout_time = 60
        while True:
            if self.player.dropout_time < dropout_time:
                text = "PINGO;"
                # print("sending ping request, player_id:{}".format(self.player.player_id))
                self.send(text)
                with ping_lock:
                    self.player.dropout_time += 1
                time.sleep(1)
            else:
                print("Client with player_id:{} has not responded to PINGO for {} seconds.".format(self.player.player_id,self.player.dropout_time))
                return
    
    def send(self,text):
        # print("sending:"+text)
        self.socket.sendto(bytes(text, 'utf-8'), self.address)

    # dispatch incoming player commands
    def msg_received(self,text):
        # print("UDP: received:"+text)
        request_dispatcher(self, text)

    def send_game_info(self):
        to_send = ""
        for rid, rival in game.game_instance.players.items():
            to_send += "MOVED:{},{},{},{},{};".format(self.sent_packet_id, rid, rival.pos_x, rival.pos_y, rival.angle)
            self.sent_packet_id += 1
            if(len(to_send) > 400):
                self.send(to_send)
                to_send = ""

            
        for b_id, current_bullet in game.game_instance.bullets.items():
            to_send += "SHOTT:{},{},{},{},{};".format(b_id,
                                                      current_bullet.body.position[0],
                                                      current_bullet.body.position[1],
                                                      current_bullet.angle,
                                                      current_bullet.speed)
            self.sent_packet_id += 1
            if (len(to_send) > 400):
                self.send(to_send)
                to_send = ""

        # print(to_send)
        self.send(to_send)


def new_connection(address):
    
    with game.game_instance.clients_lock:
        if address not in game.game_instance.clients:
            print("new connection will commence")
            c = Client(address)
            game.game_instance.clients[address] = c
        else:
            print("no new connection")
