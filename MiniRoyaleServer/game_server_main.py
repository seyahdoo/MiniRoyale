import socket
import threading
import time
import client
import game
import argparse

IP = "0.0.0.0"
PORT = 11999


def connection_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # internet, UDP
    sock.bind((IP, PORT))

    print("Server started at {} port {}".format(IP, PORT))
    
    while True:
        data, address = sock.recvfrom(1024)  # buffer size is 1024 bytes
        text = data.decode('utf-8')
        # print ("received message:"+text+"|from:"+str(address))
        if text[0:5] == "CNNRQ":
            # create new connection
            # that will deal with itself
            client.new_connection(address)
            # DONE
    

if __name__ == "__main__":

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-address", nargs='?', default=("192.168.1.4", 19998))
    args = parser.parse_args()

    # PORT = int(args.port)

    # initialize game
    game.game_init()

    # listen for connections
    connection_server_thread = threading.Thread(target=connection_server)
    connection_server_thread.daemon = True

    try:
        connection_server_thread.start()
        while True:
            time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        exit()
exit()
