from Inventory.inventory import Inventory
import random
import game
import bullet
import pymunk
from math import radians
from pymunk import Vec2d
from math import degrees

class Player:
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.movement_speed = 0
        
        self.angle = float(0)
        
        self.dropout_time = 0
        self.last_packet_id = 0
        self.sent_packet_id = 0
        
        self.current_weapon_in_hand = None
        # generate random player id and add it to the list
        player_id = random.randint(1, 5000)
        with game.game_instance.players_lock:
            while player_id in game.game_instance.players:
                player_id = random.randint(1, 5000)
            game.game_instance.players[player_id] = self
            self.player_id = player_id
        
        self.inventory = Inventory()
        print("player initiated, id:{}".format(self.player_id))
        self.add_cheat_items_for_testing()

        # Pymunk stuff
        self.body = pymunk.Body(500, pymunk.inf)
        self.body.position = (self.pos_x, self.pos_y)

        # 0.6 1.1
        self.shape = pymunk.Circle(self.body, 0.55)
        self.shape.elasticity = 0
        self.shape.collision_type = game.collision_types["player"]
        self.body.position = Vec2d(0, 0)
        game.game_instance.space.add(self.body, self.shape)
        
    def move(self, packet_id, pos_x, pos_y, angle):
        # print("player_id:{} trying to move to ({},{})".format(str(self.player_id), str(pos_x), str(pos_y)))
        # check speed

        # TODO make pysics engine deal with this.

        # drop packet id
        if self.last_packet_id > int(packet_id):
            return
        else:
            self.last_packet_id = int(packet_id)
            # can use dropout_time = 0 
        try:
            # self.pos_x = float(pos_x)
            # self.pos_y = float(pos_y)
            # self.angle = (float(angle) % 360)
            self.body.position = Vec2d(float(pos_x), float(pos_y))
            self.body.angle = radians(float(angle))
        except:
            print("Error: Can not parse position info. Playerid:{} ".format(self.player_id))
            
        # print("player_id:{} current position ({},{})".format(str(self.player_id), str(self.pos_x), str(self.pos_y)))
        
    def add_cheat_items_for_testing(self):
        weapon_id = random.randint(1, 5000)
        self.inventory.add_item(weapon_id)
        self.current_weapon_in_hand = self.inventory.equipped_items[weapon_id]
        print("Weapon with weapon_id:{} and weapon_type:{} is currenty equipped in main hand".format(self.current_weapon_in_hand.item_id,self.current_weapon_in_hand.item_type_id))
        
    def shoot(self):
        weapon_type_id = self.current_weapon_in_hand.item_type_id
            
        if weapon_type_id == 1001:
            # 32 is the game tick rate
            speed = 15
            damage = 15
        elif weapon_type_id == 1002:
            speed = 15
            damage = 20

        bullet.Bullet(self.player_id, self.body.position[0], self.body.position[1], degrees(self.body.angle), speed, damage)
