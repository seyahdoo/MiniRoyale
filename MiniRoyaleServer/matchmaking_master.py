import socket
import threading
import time
import argparse
import os

import subprocess

IP = "0.0.0.0"
PORT = 11999

REMOTE_IP = "192.168.1.2"
REMOTE_PORT = 11998

# server settings
ServerMaxPlayerSize = 30
ServerStartTime = 50

LastServerIP = ""
LastServerPort = 0
LastServerPopulation = 0
LastServerCreateTime = 0

sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def connection_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # internet, UDP
    sock.bind((IP, PORT))

    print("Matchmaking Master Server started at {} port {}".format(IP, PORT))

    while True:
        data, address = sock.recvfrom(1024)  # buffer size is 1024 bytes
        text = data.decode('utf-8')
        print ("received message:"+text+"|from:"+str(address))
        if text[0:5] == "MATCH":
            # create a game if not present
            print("tried to connect properly")
            connect_one(address)


def connect_one(address):

    if LastServerPopulation == 0 or LastServerCreateTime + ServerStartTime < time.time():
        # create server
        # TODO random_port =
        subprocess.Popen(["venv\Scripts\python", "game_server_main.py", "-port=11998"])
        # TODO get remote ip

    print("FOUND!, {}".format(address))
    sender_socket.sendto(bytes("FOUND:{},{};".format(REMOTE_IP,REMOTE_PORT), 'utf-8'), address)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-port", nargs='?', default=11999)
    args = parser.parse_args()

    PORT = int(args.port)

    connection_server_thread = threading.Thread(target=connection_server)
    connection_server_thread.daemon = True

    try:
        connection_server_thread.start()
        while True:
            time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        exit()
exit()
