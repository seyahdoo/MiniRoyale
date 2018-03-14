import socket
import threading
import time

import Client

def ConnectionServer():
    UDP_IP = "0.0.0.0"
    UDP_PORT = 11999 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #internet, UDP
    sock.bind((UDP_IP, UDP_PORT))

    print("Server started at {} port {}".format(UDP_IP, UDP_PORT))
    
    while True:        
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        text = data.decode('utf-8')
        print ("received message:"+text+"|from:"+str(addr))
        if(text[0,4] == "CONCT"):
            #create new connection
            #that will deal with itself
            Client.new_connection(addr)
            #DONE
    

if __name__ == "__main__":

    connection_server_thread = threading.Thread(target=ConnectionServer)
    connection_server_thread.daemon = True

    try:
        connection_server_thread.start()
        while True: time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        exit()
exit()