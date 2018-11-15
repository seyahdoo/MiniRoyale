import socket
import threading
import argparse
import subprocess
import time
from requests import get

# Use this later
# from requests import get
#
# ip = get('https://api.ipify.org').text
# print('My public IP address is: {}'.format(ip))

IP = "0.0.0.0"
PORT = 0

ServerMaxPlayerSize = 30
ServerStartTime = 50

games = []
games_lock = threading.Lock()

last_game_server_ip = ""
last_game_server_port = 0
last_game_server_population = 0
last_game_server_creation_time = 0
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# find master adress
master_ip = socket.gethostbyname('master1.royale.seyahdoo.com')

# find my adress
# my_ip = get('https://api.ipify.org').text
# TODO delete this and use proper one (this is for testing only)
my_ip = "192.168.1.22"


def connection_server():

    global PORT

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # internet, UDP
    sock.bind((IP, PORT))
    PORT = sock.getsockname()[1]
    address = IP, PORT

    print("Slave started at {} port {}".format(IP, PORT))

    # send info to master
    sender_socket.sendto(
        bytes("SLAVS:{},{};".format(my_ip, PORT), 'utf-8'),
        (master_ip, 11999))

    while True:
        data, address = sock.recvfrom(1024)  # buffer size is 1024 bytes
        text = data.decode('utf-8')
        print ("received message:"+text+"|from:"+str(address))
        for cmd in text.split(";"):
            if cmd[0:5] == "MATCH":
                # create a game if not present
                arguments = cmd[6:]
                arguments = arguments.split(',')

                connect_one(arguments[0], arguments[1])
                print("tried to connect properly")

            # Game Created
            # TODO Noo need, now we use PIPES(from os)
            elif cmd[0:5] == "GAMEC":
                pass
                #print("FOUND:{},{};".format(last_game_server_ip, last_game_server_port))
                #sender_socket.sendto(
                #    bytes("FOUND:{},{};".format(last_game_server_ip, last_game_server_port), 'utf-8'),
                #    client_address)


def connect_one(client_ip, client_port):
    client_address = client_ip, client_port

    global last_game_server_creation_time
    global last_game_server_population

    if \
            len(games) <= 0 or\
            last_game_server_creation_time + ServerStartTime < time.time() or\
            last_game_server_population >= ServerMaxPlayerSize:

        # print("Printing time.time: ", time.time())
        last_game_server_creation_time = time.time()
        last_game_server_population = 0

        game_port = create_game()
        games.append(game_port)

    # TODO logically select a proper game
    selected_game_port = games[0]
    #FOUND: ipaddr, port;
    print("Sending -> " + "FOUND:{},{};".format(my_ip, selected_game_port))
    sender_socket.sendto(
        bytes("FOUND:{},{};".format(my_ip, selected_game_port), 'utf-8'),
        (client_ip, int(client_port)))

def create_game():
    process = subprocess.Popen(["venv\Scripts\python", "game_server_main.py", "-address={}".format((IP,PORT))],stdout=subprocess.PIPE)
    for line in iter(process.stdout.readline, ''):
        cmd = line[0:4].decode()
        if cmd == "PORT":
            return int(line[5:-2].decode())

    return


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-port", nargs='?', default=0)
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
