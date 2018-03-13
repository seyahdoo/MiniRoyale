import socketserver
import threading
import time


clientDictionary = {}

def getRequestType(buffer, address, host):
    print(buffer)
    
    if(buffer[:4] == "JOIN")
        


class PlayerInformation:
   # int playerId
   # int port
   # float posX, posY, playerMovementSpeedMultiplier
  #  string host
    
    def __init__(self,playerId,host,port):
        self.host = host
        self.port = port
        self.playerId = playerId
    
    

class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
# Clientlari dictionary ile sınıfla

    def handle(self):
        global clientDictionary
        key = self.client_address
        
        data = self.request[0].strip()
        socket = self.request[1]
        
        if key in clientDictionary:
            print('Client already in dictionary.')
            print("{}: client: {}, wrote:{}".format(threading.current_thread().name, self.client_address, data))

        else:

            current_thread = threading.current_thread()
            clientDictionary = {key: current_thread}
            print('New client, adding to dictionary.')
            print("{}: client: {}, wrote:{}".format(current_thread.name, self.client_address, data))

        print(threading.active_count())


        socket.sendto(data.upper(), self.client_address)
        #print(type(self.client_address))
class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 11999
    
    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True

    try:
        server_thread.start()
        print("Server started at {} port {}".format(HOST, PORT))
        while True: time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()
        server.server_close()
exit()