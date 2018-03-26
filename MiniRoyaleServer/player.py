import sys
sys.path.append('./Inventory')
import inventory    # import your stuffimport os

#wd = os.getcwd()    # save current working directory
#os.chdir('./Inventory')    # change to directory containing main.py  
#import inventory    # import your stuff
#os.chdir(wd)    # change back to directory containing sub.pyimport random

import random
import game
import bullet

class Player():
    
    def __init__(self):
        
        self.posx = 0
        self.posy = 0
        self.movement_speed = 0
        
        self.rotation = float(0)
        
        self.dropout_time = 0
        self.last_packet_id = 0
        self.sent_packet_id = 0
        
        self.current_weapon_in_hand = None
        # generate random player id and add it to the list
        player_id = random.randint(1,5000)
        with game.game_instance.players_lock:
            while player_id in game.game_instance.players:
                player_id = random.randint(1,5000)
            game.game_instance.players[player_id] = self
            self.player_id = player_id
        
        self.inventory = inventory.Inventory()
        print("player initiated, id:{}".format(self.player_id))
        self.addCheatItemsForTesting()
        
    def Move(self,packet_id,posx,posy,rotation):
        #print("playerid:{} trying to move to ({},{})".format(str(self.player_id), str(posx), str(posy)))
        #check speed
        
        #drop packet id
        if self.last_packet_id > int(packet_id):
            return
        else:
            self.last_packet_id = int(packet_id)
            # can use dropout_time = 0 
        try:
            self.posx = float(posx)
            self.posy = float(posy)
            self.rotation = (float(rotation) % 360)

            
        except:
            print("Error: Can not parse position info. Playerid:{} ".format(self.player_id))
            
        
        #print("playerid:{} current position ({},{})".format(str(self.player_id), str(self.posx), str(self.posy)))
        

    def addCheatItemsForTesting(self):
        weapon_id = random.randint(1,5000)
        self.inventory.addItem(weapon_id)
        self.current_weapon_in_hand = self.inventory.equipped_items[weapon_id]
        print("Weapon with weapon_id:{} and weapon_type:{} is currenty equipped in main hand".format(self.current_weapon_in_hand.item_id,self.current_weapon_in_hand.item_type_id))
        
    def shoot(self):
        weapon_type_id = self.current_weapon_in_hand.item_type_id
            
        if weapon_type_id == 1001:
            # 32 is the game tick rate
            speed = 5
            damage = 15
        elif weapon_type_id == 1002:
            speed = 5
            damage = 20
           
        bullet.Bullet(self.player_id,self.posx,self.posy,self.rotation,speed,damage)
        
        
    #def send_ping(self,client):
       # text = ""
       # for rid, rival in game.game_instance.players.items():
       #     text += "PINGO;"
       #     print("sending ping request, player_id:{}".format(self.game_instance.players[0]))
      #  client.send(bytes(text, 'utf-8'), client)
        
        
        
        