import threading
import socket
import time
import player
import bullet
from request_dispatcher import request_dispatcher
from player import Player
from math import degrees

clients = {}
clients_to_be_added = []
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
        # TODO not any ip, player ip DAMN!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.server_ip = "0.0.0.0"
        # Random available Port
        self.server_port = 0  # random write zero here
        # One socket for each client
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # internet, UDP
        # Bind socket and generate a new open port
        self.socket.bind((self.server_ip, self.server_port))
        # Store generated port
        self.server_port = self.socket.getsockname()[1]  # new port

        # create or login a player
        self.player = Player(self)
        print("created Player for Client, player_id:{}".format(self.player.player_id))
        self.send("PIREQ:" + player.get_player_info_command_message(self.player.player_id))

        # listen with a new thread
        self.listener_thread = threading.Thread(target=self.listener)
        self.listener_thread.daemon = True
        self.listener_thread.start()
        # print("Before sending port")

        # Send newly generated socket info to client
        self.send("PORTO:" + str(self.server_port) + ";")
        print("PORTO:" + str(self.server_port) + ";")

        # create ping thread
        self.ping_thread = threading.Thread(target=self.ping_routine)
        self.ping_thread.daemon = True
        self.ping_thread.start()

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
                # TODO terminate client
                return

    def send(self,text):
        # print("UDP:Sending:"+text)
        self.socket.sendto(bytes(text, 'utf-8'), self.address)

    # dispatch incoming player commands
    def msg_received(self,text):
        # print("UDP:Received:"+text)
        request_dispatcher(self, text)

    def send_game_info(self):

        # TODO send spawned item information to player

        to_send = ""
        for rid, rival in player.players.items():
            to_send += "MOVED:{},{},{},{},{};".format(self.sent_packet_id, rid, rival.body.position[0], rival.body.position[1], degrees(rival.body.angle))
            self.sent_packet_id += 1
            if len(to_send) > 400:
                self.send(to_send)
                to_send = ""

        for b_id, current_bullet in bullet.bullets.items():
            to_send += "SHOTT:{},{},{},{},{};".format(b_id,
                                                      current_bullet.body.position[0],
                                                      current_bullet.body.position[1],
                                                      current_bullet.angle,
                                                      current_bullet.speed)
            self.sent_packet_id += 1
            if len(to_send) > 400:
                self.send(to_send)
                to_send = ""

        # print(to_send)
        self.send(to_send)


def new_connection(address):
    global clients
    global clients_to_be_added

    if address not in clients:
        print("new connection will commence")
        c = Client(address)
        clients_to_be_added.append(c)
    else:
        print("no new connection")


def send_game_info_to_all_clients():
    # TODO Implement thread safe client
    global clients
    for current_client in clients.values():
        current_client.send_game_info()


def send_message_to_nearby_clients(pos_x, pos_y, message):
    global clients
    for current_client in clients.values():
        current_client.send(message)
        # print(message)
    # TODO optimize this


def send_winner_information_to_all_players(winner_player):
    # global clients
    #
    # for current_client in clients.values():
    #     current_client.send()
    pass


def add_clients_to_be_added():
    global clients_to_be_added
    global clients

    for current_client in clients_to_be_added:
        clients[current_client.address] = current_client

    clients_to_be_added = []
