import game
import physics
import client
import pymunk
import threading
from pymunk import Vec2d
from math import radians

bullets = {}
bullets_to_be_updated = {}
bullets_lock = threading.RLock()

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

        with bullets_lock:
            global bullets

            game.game_instance.prop_id_counter += 1
            bullet_id = game.game_instance.prop_id_counter

            self.bullet_id = bullet_id

            with physics.physics_lock:
                physics.space.add(self.body, self.shape)

            bullets[bullet_id] = self
        
    def update(self):
        # Delete bullet in 3 seconds
        bullet_delete_timer = 3
        if self.frame_count < game.game_instance.tick_rate * bullet_delete_timer:
            self.frame_count += 1
            return True
        else:
            print("Trying to delete bullet_id:{}".format(self.bullet_id))

            with bullets_lock:
                deleted_bullet_info = "DELBL:{};".format(self.bullet_id)
                deleted_bullet_pos_x = self.body.position[0]
                deleted_bullet_pos_y = self.body.position[1]

                with physics.physics_lock:
                    physics.space.remove(self.body, self.shape)

                del bullets[self.bullet_id]

                client.send_message_to_nearby_clients(deleted_bullet_pos_x, deleted_bullet_pos_y, deleted_bullet_info)

            # Mark for delete
            # bullet_indexes_to_be_deleted.append(self.bullet_id)

            # TODO DELETE -> Send player info
            return False


def update_bullet_state():
    global bullets, bullets_to_be_updated
    bullets_to_be_updated = bullets.copy()

    with bullets_lock:
        for current_bullet in bullets_to_be_updated.values():
            current_bullet.update()

    bullets_to_be_updated = {}
