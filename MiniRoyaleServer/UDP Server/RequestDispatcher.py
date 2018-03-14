
playerDictionary = {}

class PlayerInformation:
   # int playerId
   # int port
   # float posX, posY, playerMovementSpeedMultiplier
  #  string host
    
    def __init__(self,playerId,host,port):
        self.host = host
        self.port = port
        self.playerId = playerId
    


def getRequestType(buffer, address, host):
    global playerDictionary
    
    commands = buffer.split(';')
    
    for command in commands:
        print('received: '+buffer)
        cmd = buffer[:4]
        
        if(cmd == "JOIN"):
            pid = buffer[5:-1]
            print(pid)
            print('joined '+pid)



def Dispatch (data, fromadress, socket):
    print('try to distpatch')
    
    socket.sendto(data.upper(), fromadress)
    
