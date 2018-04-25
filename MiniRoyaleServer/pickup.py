import physics
import pymunk
import threading

pickup_id_counter = 0

pickups = {}
pickup_lock = threading.Lock()

pickup_shape_to_pickup = {}


class Pickup:
    def __init__(self, pos_x, pos_y, quantity, item_type):
        self.quantity = quantity
        self.item_type = item_type

        self.body = pymunk.Body(1, pymunk.inf)
        self.body.position = (float(pos_x), float(pos_y))

        self.shape = pymunk.Circle(self.body, 0.3)
        self.shape.elasticity = 0.0
        self.shape.collision_type = physics.collision_types["pickup"]

        pickup_shape_to_pickup[self.shape] = self

        with pickup_lock:
            global pickup_id_counter
            pickup_id_counter += 1
            self.pickup_id = pickup_id_counter

            with physics.physics_lock:
                physics.space.add(self.body, self.shape)

            pickups[self.pickup_id] = self
