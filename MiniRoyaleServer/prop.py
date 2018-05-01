import threading
import pymunk
import physics
import random
from pymunk import Vec2d
from math import radians

prop_id_count = 10000
prop_id_count_lock = threading.Lock()

props = {}
props_lock = threading.Lock()

prop_shape_to_prop = {}

prop_types = {
    7001: ('rectangle', (1, 1)),
    7002: ('circle', 1),
}


class Prop:

    def __init__(self, is_dynamic, prop_type, pos_x, pos_y):
        self.is_dynamic = is_dynamic

        with prop_id_count_lock:
            global prop_id_count
            prop_id_count += 1
            self.prop_id = prop_id_count

        self.prop_type = prop_type
        self.body_type = prop_types[prop_type][0]
        self.health = 50

        # physics stuff
        self.body = None
        self.shape = None
        self.create_body()
        self.body.position = Vec2d(float(pos_x), float(pos_y))
        with props_lock:
            global props
            self.create_body()
            props[self.prop_id] = self

    def create_body(self):

        if self.body_type == 'rectangle':
            if self.is_dynamic:
                self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
            else:
                self.body = pymunk.Body(body_type=pymunk.Body.STATIC)

            self.shape = pymunk.Poly.create_box(self.body, (float(prop_types[self.prop_type][1][0]), float(prop_types[self.prop_type][1][1])))

        elif self.body_type == 'circle':
            self.body = pymunk.Body(100, pymunk.inf)
            self.shape = pymunk.Circle(self.body, float(prop_types[self.prop_type][1]))

        self.shape.elasticity = 0.0
        self.shape.collision_type = physics.collision_types["prop"]

        self.body.angle = radians(float(random.uniform(0, 360)))
        prop_shape_to_prop[self.shape] = self

        with physics.physics_lock:
            physics.space.add(self.body, self.shape)
