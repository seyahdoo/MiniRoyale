import random

import game

class Player():
    
    def __init__(self):
        
        self.posx = 0
        self.posy = 0
        self.movement_speed = 0
        
        #self.still_connected = 1
        self.last_packet_id = 0
        self.sent_packet_id = 0
        # generate random player id and add it to the list
        player_id = random.randint(1,5000)
        with game.game_instance.players_lock:
            while player_id in game.game_instance.players:
                player_id = random.randint(1,5000)
            game.game_instance.players[player_id] = self
            self.player_id = player_id
        
        
        print("player initiated, id:{}".format(self.player_id))
        
        
    def Move(self,packet_id,posx,posy):
        #print("playerid:{} trying to move to ({},{})".format(str(self.player_id), str(posx), str(posy)))
        #check speed
        
        #drop packet id
        if self.last_packet_id > int(packet_id):
            return
        else:
            self.last_packet_id = int(packet_id)
        
        try:
            self.posx = float(posx)
            self.posy = float(posy)
        except:
            print("Error: not a float number. Playerid:{} ".format(self.player_id))
            
        
        #print("playerid:{} current position ({},{})".format(str(self.player_id), str(self.posx), str(self.posy)))
        
    
    def GetInfo(self,client):
        
        tosend = ""
        for rid, rival in game.game_instance.players.items():
            tosend += "MOVED:{},{},{},{};".format(self.sent_packet_id,rid,rival.posx,rival.posy)
        self.sent_packet_id += 1
        client.send(tosend)
        
    #def send_ping(self,client):
       # text = ""
       # for rid, rival in game.game_instance.players.items():
       #     text += "PINGO;"
       #     print("sending ping request, player_id:{}".format(self.game_instance.players[0]))
      #  client.send(bytes(text, 'utf-8'), client)
        
        
        
        