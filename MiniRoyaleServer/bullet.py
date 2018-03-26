
import random
import game

from math import cos
from math import sin

class Bullet:
    def __init__(self,player_id,posx,posy,rotation,speed,damage):
        self.player_id = int(player_id)
        self.posx = posx
        self.posy = posy
        self.rotation = rotation
        self.speed = speed
        self.damage = damage
        
        self.frame_count = 0
        
        bullet_id = random.randint(1,15000)
        while game.game_instance.bullets.get(bullet_id) is not None:
            bullet_id = random.randint(1,15000)
        self.bullet_id = bullet_id
        game.game_instance.bullets[self.bullet_id] = self
        
        print("Succesfully created bullet from player_id:{}".format(self.player_id))
        
    def update(self):
        if self.frame_count < game.game_instance.tickrate * 20:
            new_posx = self.posx + (cos(self.rotation) * self.speed * 1/game.game_instance.tickrate)
            new_posy = self.posy + (sin(self.rotation) * self.speed * 1/game.game_instance.tickrate)
     
            self.posx = new_posx
            self.posy = new_posy
            self.frame_count += 1
            return True
        else:
            print("Trying to delete bullet_id:{}".format(self.bullet_id))
            #game.game_instance.bullets.pop(self.bullet_id,None)
            #print("Succesfully deleted bullet!")
            return False
        
