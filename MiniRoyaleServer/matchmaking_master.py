import socket
import threading
import time
import argparse
import matchmaking_slave
import subprocess
import random


IP = "0.0.0.0"
PORT = 11999

REMOTE_IP = "192.168.1.22"
REMOTE_PORT = 11998

# server settings
ServerMaxPlayerSize = 30
ServerStartTime = 50

LastServerIP = ""
LastServerPort = 0
LastServerPopulation = 0
LastServerCreateTime = 0

sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

slaves = []


def master_connection_listener():
    global slaves
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # internet, UDP
    sock.bind((IP, PORT))

    print("Matchmaking Master Server started at {} port {}".format(IP, PORT))

    while True:
        data, address = sock.recvfrom(1024)  # buffer size is 1024 bytes
        text = data.decode('utf-8')
        print("received message:"+text+"|from:"+str(address))
        if text[0:5] == "MATCH":
            # create a game if not present
            print("tried to connect properly")
            get_service_provider(address)
        elif text[0:5] == "SLAVS":
            arguments = text[6:]
            arguments = arguments.split(',')
            slaves.append((arguments[0], arguments[1]))
            pass


def get_service_provider(address):

    if len(slaves) == 0:
        # TODO Create a slave if not exist
        pass

    request = "MATCH:{},{};".format(address[0], address[1])

    # TODO make o load balancer for selecting slave
    selected_slave_address = random.choice(list(slaves))
    sender_socket.sendto(bytes(request, 'utf-8'), selected_slave_address)


def create_slave():
    # TODO create slave machine from AWS using AWS api
    pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-port", nargs='?', default=11999)
    args = parser.parse_args()

    PORT = int(args.port)

    connection_server_thread = threading.Thread(target=master_connection_listener)
    connection_server_thread.daemon = True

    try:
        connection_server_thread.start()
        while True:
            time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        exit()
exit()
