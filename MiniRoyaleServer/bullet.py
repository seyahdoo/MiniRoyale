import game
import physics
import client
import pymunk
from pymunk import Vec2d
from math import radians

bullets = {}
bullets_to_be_spawned = []
bullet_indexes_to_be_deleted = []

bullet_shape_to_bullet = {}


class Bullet:
    def __init__(self, player_id, pos_x, pos_y, angle, speed, damage):
        global bullets_to_be_spawned

        self.player_id = int(player_id)
        self.speed = speed
        self.damage = damage

        self.angle = angle

        self.frame_count = 0

        # physics stuff
        self.body = pymunk.Body(1, pymunk.inf)
        self.body.position = (pos_x, pos_y)

        self.shape = pymunk.Circle(self.body, 0.2)
        self.shape.elasticity = 1.0
        self.shape.collision_type = physics.collision_types["bullet"]

        bullet_shape_to_bullet[self.shape] = self

        impulse = Vec2d(1, 0)
        impulse.rotate(radians(angle))
        self.body.apply_impulse_at_local_point(impulse, self.body.position)

        # Keep bullet velocity at a static value
        def constant_velocity(body, gravity, damping, dt):
            body.velocity = body.velocity.normalized() * self.speed

        self.body.velocity_func = constant_velocity
        ###

        bullets_to_be_spawned.append(self)
        #print("Successfully created bullet from player_id:{}".format(self.player_id))
        
    def update(self):
        # Delete bullet in 3 seconds
        bullet_delete_timer = 3
        if self.frame_count < game.game_instance.tick_rate * bullet_delete_timer:
            self.frame_count += 1
            return True
        else:
            print("Trying to delete bullet_id:{}".format(self.bullet_id))

            # Mark for delete
            bullet_indexes_to_be_deleted.append(self.bullet_id)

            # TODO DELETE -> Send player info
            return False


def spawn_bullets_to_be_spawned():
    global bullets_to_be_spawned
    global bullets
    for current_bullet in bullets_to_be_spawned:
        game.game_instance.prop_id_counter += 1
        bullet_id = game.game_instance.prop_id_counter
        current_bullet.bullet_id = bullet_id

        bullets[bullet_id] = current_bullet
        physics.space.add(current_bullet.body, current_bullet.shape)
    bullets_to_be_spawned = []


def update_bullet_state():
    global bullets
    for current_bullet in bullets.values():
        current_bullet.update()


# TODO send DELBL information to client
def delete_marked_bullets():
    global bullets
    global bullet_indexes_to_be_deleted
    for i in bullet_indexes_to_be_deleted:
        # Store the bullet to be deleted next's information
        deleted_bullet_info = "DELBL:{};".format(bullets[i].bullet_id)
        deleted_bullet_pos_x = bullets[i].body.position[0]
        deleted_bullet_pos_y = bullets[i].body.position[1]
        # Delete the bullet first
        physics.space.remove(bullets[i].body, bullets[i].shape)
        del bullets[i]
        # Then send information of the deleted bullet
        client.send_message_to_nearby_clients(deleted_bullet_pos_x, deleted_bullet_pos_y, deleted_bullet_info)
        # print("Successfully deleted bullet")
    bullet_indexes_to_be_deleted = []
