import random
import game

import  pymunk
from pymunk import Vec2d

from math import cos
from math import sin


class Bullet:
    def __init__(self, player_id, pos_x, pos_y, angle, speed, damage):
        self.player_id = int(player_id)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.angle = angle
        self.speed = speed
        self.damage = damage
        
        self.frame_count = 0
        
        bullet_id = random.randint(1, 15000)
        while game.game_instance.bullets.get(bullet_id) is not None:
            bullet_id = random.randint(1, 15000)
        self.bullet_id = bullet_id
        game.game_instance.bullets[self.bullet_id] = self

        ###
        self.body = pymunk.Body(1, pymunk.inf)
        self.body.position = (self.pos_x, self.pos_y)

        self.shape = pymunk.Circle(self.body, 0.2)
        self.shape.elasticity = 1.0
        self.shape.collision_type = game.collision_types["bullet"]

        #self.body.apply_impulse_at_local_point(Vec2d((cos(self.angle),sin(self.angle))))

        # Keep bullet velocity at a static value
        def constant_velocity(body, gravity, damping, dt):
            body.velocity = body.velocity.normalized() * 400

        self.body.velocity_func = constant_velocity

        game.game_instance.space.add(self.body, self.shape)

        ###

        print("Successfully created bullet from player_id:{}".format(self.player_id))
        
    def update(self):
        if self.frame_count < game.game_instance.tick_rate * 20:
            # TODO DELETE -> Moved to physics
            #new_pos_x = self.pos_x + (cos(self.rotation) * self.speed * 1 / game.game_instance.tickrate)
            #new_pos_y = self.pos_y + (sin(self.rotation) * self.speed * 1 / game.game_instance.tickrate)
     
            #self.pos_x = new_pos_x
            #self.pos_y = new_pos_y

            self.frame_count += 1
            return True
        else:
            print("Trying to delete bullet_id:{}".format(self.bullet_id))
            # game.game_instance.bullets.pop(self.bullet_id,None)
            # print("Successfully deleted bullet!")
            return False
