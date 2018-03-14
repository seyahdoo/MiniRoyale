import random

import game

class Player():
    
    def __init__(self):
        
        self.posx = 0
        self.posy = 0
        self.movement_speed = 0
        
        # generate random player id and add it to the list
        player_id = random.randint(1,5000)
        with game.game_instance.players_lock:
            while player_id in game.game_instance.players:
                player_id = random.randint(1,5000)
            game.game_instance.players[player_id] = self
            self.player_id = player_id
        
        
        print("player initiated, id:{}".format(self.player_id))
        
        
    def Move(self,posx,posy):
        print("playerid:{} trying to move to ({},{})".format(str(self.player_id), str(posx), str(posy)))
        #check speed
        
        #drop packet id
        
        try:
            self.posx = float(posx)
            self.posy = float(posy)
        except:
            print("Error: not a float number. Playerid:{} ".format(self.player_id))
            
        
        print("playerid:{} current position ({},{})".format(str(self.player_id), str(self.posx), str(self.posy)))
        
    
    def GetInfo(self,client):
        
        tosend = ""
        for rid, rival in game.game_instance.players.items():
            tosend += "MOVED:0,{},{},{};".format(rid,rival.posx,rival.posy)
        
        client.send(tosend)
        
        
        
        