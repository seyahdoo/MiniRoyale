import socket
import threading
import time
import client
import game


def connection_server():
    udp_ip = "0.0.0.0"
    udp_port = 11999
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # internet, UDP
    sock.bind((udp_ip, udp_port))

    print("Server started at {} port {}".format(udp_ip, udp_port))
    
    while True:
        data, address = sock.recvfrom(1024) # buffer size is 1024 bytes
        text = data.decode('utf-8')
        # print ("received message:"+text+"|from:"+str(address))
        if text[0:5] == "CNNRQ":
            # create new connection
            # that will deal with itself
            client.new_connection(address)
            # DONE
    

if __name__ == "__main__":

    game.game_init()

    connection_server_thread = threading.Thread(target=connection_server)
    connection_server_thread.daemon = True

    try:
        connection_server_thread.start()
        while True: time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        exit()
exit()
