import game
import physics
import client
import pymunk
import threading
from pymunk import Vec2d
from math import radians
import sys

bullets = {}
bullets_to_be_updated = {}
bullets_lock = threading.RLock()

bullet_shape_to_bullet = {}

bullet_id_counter_lock = threading.Lock()
bullet_id_counter = 10000


class Bullet:

    def __init__(self, player_id, pos_x, pos_y, angle, speed, damage):

        self.player_id = int(player_id)
        self.speed = speed
        self.damage = damage

        self.angle = angle

        self.frame_count = 0

        # physics stuff
        self.body = pymunk.Body(1, pymunk.inf)
        self.body.position = (pos_x, pos_y)

        self.shape = pymunk.Circle(self.body, 0.1)
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
        # print("-> Entering bullet lock from bullet, trying to create bullet")
        sys.stdout.flush()
        with bullets_lock:
            # print("- entered bullet lock from bullet, trying to create bullet")
            global bullets
            global bullet_id_counter

            with bullet_id_counter_lock:
                bullet_id_counter += 1
                self.bullet_id = bullet_id_counter

            with physics.physics_lock:
                physics.space.add(self.body, self.shape)

            bullets[self.bullet_id] = self
        # print("<- exiting bullet lock from bullet, trying to create bullet")

    def update(self):
        # Delete bullet in 3 seconds
        bullet_delete_timer = 3
        if self.frame_count < game.game_instance.tick_rate * bullet_delete_timer:
            self.frame_count += 1
            return True
        else:
            # print("Trying to delete bullet_id:{}".format(self.bullet_id))
            # print("-> Entering bullet lock from bullet, trying to update bullet")
            sys.stdout.flush()
            with bullets_lock:
                # print("- entered bullet lock from bullet, trying to update bullet")
                deleted_bullet_info = "DELBL:{};".format(self.bullet_id)
                deleted_bullet_pos_x = self.body.position[0]
                deleted_bullet_pos_y = self.body.position[1]

                if self.bullet_id in bullets:
                    with physics.physics_lock:
                        physics.space.remove(self.body, self.shape)
                    del bullets[self.bullet_id]
                    client.send_message_to_nearby_clients(deleted_bullet_pos_x, deleted_bullet_pos_y, deleted_bullet_info)
            # print("<- exiting bullet lock from bullet, trying to update bullet")
            # Mark for delete
            # bullet_indexes_to_be_deleted.append(self.bullet_id)

            # TODO DELETE -> Send player info
            return False


def update_bullet_state():
    global bullets, bullets_to_be_updated
    # print("-> Entering bullet lock from bullet, trying to update bullet state")
    sys.stdout.flush()
    with bullets_lock:
        # print("- entered  bullet lock from bullet, trying to update bullet state")
        bullets_to_be_updated = bullets.copy()
        for current_bullet in bullets_to_be_updated.values():
            current_bullet.update()
    # print("<- exiting bullet lock from bullet, trying to update bullet state")
    bullets_to_be_updated = {}
