import game

import pymunk
from pymunk import Vec2d
from math import radians

bullets = {}
bullets_to_be_spawned = []
bullets_to_be_deleted = []


class Bullet:
    def __init__(self, player_id, pos_x, pos_y, angle, speed, damage):
        global bullets_to_be_spawned

        self.player_id = int(player_id)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.angle = angle
        self.speed = speed
        self.damage = damage
        
        self.frame_count = 0
        # Pymunk stuff
        self.body = pymunk.Body(1, pymunk.inf)
        self.body.position = (self.pos_x, self.pos_y)

        self.shape = pymunk.Circle(self.body, 0.2)
        self.shape.elasticity = 1.0
        self.shape.collision_type = game.collision_types["bullet"]

        impulse = Vec2d(1, 0)
        impulse.rotate(radians(self.angle))
        self.body.apply_impulse_at_local_point(impulse, self.body.position)
        # Keep bullet velocity at a static value

        def constant_velocity(body, gravity, damping, dt):
            body.velocity = body.velocity.normalized() * self.speed

        self.body.velocity_func = constant_velocity

        # game.game_instance.space.add(self.body, self.shape)

        ###

        bullets_to_be_spawned.append(self)
        print("Successfully created bullet from player_id:{}".format(self.player_id))
        
    def update(self):
        if self.frame_count < game.game_instance.tick_rate * 20:
            # TODO DELETE -> Moved to physics
            self.frame_count += 1
            return True
        else:
            print("Trying to delete bullet_id:{}".format(self.bullet_id))
            # game.game_instance.bullets.pop(self.bullet_id,None)
            # print("Successfully deleted bullet!")
            return False


def spawn_bullets_to_be_spawned():
    global bullets_to_be_spawned
    global bullets
    for current_bullet in bullets_to_be_spawned:
        game.game_instance.prop_id_counter += 1
        bullet_id = game.game_instance.prop_id_counter
        current_bullet.bullet_id = bullet_id

        bullets[bullet_id] = current_bullet
        game.game_instance.space.add(current_bullet.body, current_bullet.shape)
    bullets_to_be_spawned = []


def update_bullet_state():
    global bullets
    global bullets_to_be_deleted
    for b_id, current_bullet in bullets.items():
        if not current_bullet.update():
            # Mark for delete
            bullets_to_be_deleted.append(b_id)

# TODO send DELET information to client
def delete_marked_bullets():
    global bullets
    global bullets_to_be_deleted
    for i in bullets_to_be_deleted:
        game.game_instance.space.remove(bullets[i].body, bullets[i].shape)
        del bullets[i]
        # print("Successfully deleted bullet")
    bullets_to_be_deleted = []
