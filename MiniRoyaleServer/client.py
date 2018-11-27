import threading
import socket
import time
import player
import bullet
import pickup
import prop
import safe_zone
from request_dispatcher import request_dispatcher
from player import Player
from math import degrees

clients = {}
clients_to_be_added = []
ping_lock = threading.Lock()


class Client:

    def __init__(self, address):
        print("Client Init")

        self.disconnected = False

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
        # TODO bind to client's ip -> self.address[0]
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
        print("created Player for Client {}, player_id:{}".format(self.address, self.player.player_id))

        # Send SINFO to make client store itself's player id
        self.send("SINFO:{};".format(self.player.player_id))

        # Send PINFO to load inventory and stuff
        self.send(player.get_player_info_command_message(self.player.player_id))

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
        while not self.disconnected:
            # Receive
            try:
                data, address = self.socket.recvfrom(1024)
                # Decode message
                text = data.decode('utf-8')
                # Message Received
                self.msg_received(text)
            except:
                pass
                # print('Did not receive incoming message')

    def ping_routine(self):
        # Send ping request every 1 seconds
        # Disconnect if no answer has came for 60 seconds
        # Close main thread and delete player information in players dictionary
        dropout_time = 60
        while not self.disconnected:
            if self.player.dropout_time < dropout_time:
                text = "PINGO;"
                # print("sending ping request, player_id:{}".format(self.player.player_id))
                self.send(text)
                with ping_lock:
                    self.player.dropout_time += 1
                time.sleep(1)
            else:
                print("Client with player_id:{} has not responded to PINGO for {} seconds.".format(self.player.player_id,self.player.dropout_time))
                self.disconnect()

    def send(self, text):
        # print("UDP:Sending:"+text)
        if not self.disconnected:
            self.socket.sendto(bytes(text, 'utf-8'), self.address)

    # dispatch incoming player commands
    def msg_received(self,text):
        # print("UDP:Received:"+text)

        request_dispatcher(self, text)

    def send_game_info(self, copy_of_bullets, copy_of_players, copy_of_pickups, copy_of_props):
        to_send = ""
        if not self.disconnected:
            for rid, rival in copy_of_players.items():
                if not rival.dead:
                    to_send += "MOVED:{},{},{},{},{};".format(self.sent_packet_id, rid, rival.body.position[0], rival.body.position[1], degrees(rival.body.angle))
                    self.sent_packet_id += 1
                    if len(to_send) > 400:
                        self.send(to_send)
                        to_send = ""

            for b_id, current_bullet in copy_of_bullets.items():
                to_send += "SHOTT:{},{},{},{},{};".format(b_id,
                                                          current_bullet.body.position[0],
                                                          current_bullet.body.position[1],
                                                          current_bullet.angle,
                                                          current_bullet.speed)
                if len(to_send) > 400:
                    self.send(to_send)
                    to_send = ""

            for p_id, current_pickup in copy_of_pickups.items():
                to_send += "PCKIN:{},{},{},{},{};".format(p_id,
                                                          current_pickup.item_type,
                                                          current_pickup.body.position[0],
                                                          current_pickup.body.position[1],
                                                          current_pickup.quantity)
                if len(to_send) > 400:
                    self.send(to_send)
                    to_send = ""

            for pid, current_prop in copy_of_props.items():
                to_send += "PROPP:{},{},{},{},{};".format(current_prop.prop_id, current_prop.prop_type,
                                                          current_prop.body.position[0],
                                                          current_prop.body.position[1], degrees(current_prop.body.angle))
                if len(to_send) > 400:
                    self.send(to_send)
                    to_send = ""

            to_send += "CRCLE:{},{},{};".format(safe_zone.safe_zone_instance.pos_x,
                                                safe_zone.safe_zone_instance.pos_y,
                                                safe_zone.safe_zone_instance.radius)

            # print(to_send)
            self.send(to_send)

    def disconnect(self):
        self.disconnected = True
        self.send("EXITT;")

        # TODO fix locking issue
        self.player.client = None
        global clients
        del clients[self.address]

        print("Disconnected and deleted {} from clients list".format(self.address))


def new_connection(address):
    global clients
    global clients_to_be_added

    print("{}, client.new_connection".format(address))
    if address not in clients:
        print("new connection will commence")
        c = Client(address)
        clients_to_be_added.append(c)
    else:
        print("no new connection, reconnected")
        clients[address].disconnected = False


def send_game_info_to_all_clients():
    # TODO Implement thread safe client
    global clients

    with bullet.bullets_lock:
        copy_of_bullets = bullet.bullets.copy()
    with player.players_lock:
        copy_of_players = player.players.copy()
    with pickup.pickup_lock:
        copy_of_pickup = pickup.pickups.copy()
    with prop.props_lock:
        copy_of_props = prop.props.copy()
    # copy_of_outer_circles = safe_zone.outer_circles.copy()

    # TODO Check if this is thread safe
    for current_client in clients.values():
        current_client.send_game_info(copy_of_bullets, copy_of_players, copy_of_pickup, copy_of_props)


def send_death_info_to_all_players(death_message):
    global clients

    print(death_message)

    copy_of_clients = clients.copy()
    for current_client in copy_of_clients.values():
        current_client.send(death_message)


def send_message_to_nearby_clients(pos_x, pos_y, message):
    global clients

    copy_of_clients = clients.copy()

    for current_client in copy_of_clients.values():
        current_client.send(message)
        # print("Inside client:" + message)
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
