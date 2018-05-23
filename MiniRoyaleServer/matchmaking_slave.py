import socket
import threading
import time
import argparse
import os
import subprocess
import time


# Use this later
# from requests import get
#
# ip = get('https://api.ipify.org').text
# print('My public IP address is: {}'.format(ip))

IP = "0.0.0.0"
PORT = 11999

ServerMaxPlayerSize = 30
ServerStartTime = 50

games = {}
games_lock = threading.Lock()

master_ip = ""
master_port = 0

ip_address = master_ip
port = 0
address = "", 0

listener_thread = threading.Thread(target=connection_server)
listener_thread.daemon = True
listener_thread.start()

# Wait for port to be assigned
time.sleep(1)

last_game_server_ip = ""
last_game_server_port = 0
last_game_server_population = 0
last_game_server_creation_time = 0
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def connection_server():

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # internet, UDP
    sock.bind((ip_address, port))
    port = sock.getsockname()[1]
    address = ip_address, port

    print("Slave started at {} port {}".format(ip_address, port))

    while True:
        data, address = sock.recvfrom(1024)  # buffer size is 1024 bytes
        text = data.decode('utf-8')
        # print ("received message:"+text+"|from:"+str(address))
        if text[0:5] == "MATCH":
            # create a game if not present
            arguments = text[6:]
            arguments = arguments.split(',')

            # if last packet number is > args[0] return
            connect_one(arguments[0], arguments[1])
            print("tried to connect properly")
            connect_one(address)

        # Game Created
        elif text[0:5] == "GAMEC":

            print("FOUND:{},{};".format(last_game_server_ip, last_game_server_port))
            sender_socket.sendto(
                bytes("FOUND:{},{};".format(last_game_server_ip, last_game_server_port), 'utf-8'),
                client_address)

def connect_one(client_ip, client_port):
    client_address = client_ip, client_port

    if \
            len(games) <= 0 or\
            last_game_server_creation_time + ServerStartTime < time.time() or\
            last_game_server_population >= ServerMaxPlayerSize:

        print("Printing time.time: ", time.time())
        last_game_server_creation_time = time.time()
        last_game_server_population = 0

        subprocess.Popen(["venv\Scripts\python", "game_server_main.py", "-address={}".format(address)])


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
