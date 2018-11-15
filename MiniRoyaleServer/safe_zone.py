import pymunk
import physics
import math
import random

safe_zone_instance = None

outer_circles = []


class SafeZone:

    def __init__(self, pos_x, pos_y, outer_circle_count=36):

        self.outer_circle_count = outer_circle_count
        self.radius = 200.0 * 1.5
        self.outer_circle_radius = 5.0
        self.pos_x = 0
        self.pos_y = 0

        # physics stuff
        self.body = None
        self.shape = None

        self.create_body()

    def create_body(self):
        for i in range(0, self.outer_circle_count):

            current_circle_body = pymunk.Body(100, pymunk.inf, body_type=pymunk.Body.KINEMATIC)
            current_circle_shape = pymunk.Circle(current_circle_body, self.outer_circle_radius)

            current_circle_body.angle = (360 / self.outer_circle_count) * i

            outer_circle_pos_x = (self.radius + self.outer_circle_radius) * math.cos(current_circle_body.angle)
            outer_circle_pos_y = (self.radius + self.outer_circle_radius) * math.sin(current_circle_body.angle)

            current_circle_body.position = outer_circle_pos_x, outer_circle_pos_y

            current_circle_shape.elasticity = 1.0

            # self.shape.collision_type = physics.collision_types["prop"]


            # prop_shape_to_prop[self.shape] = self

            with physics.physics_lock:
                physics.space.add(current_circle_body, current_circle_shape)
                outer_circles.append(current_circle_body)

    def shrink_safe_zone(self):
        new_angle = float(random.uniform(0, 360))

        # When shrink_radius_by value is low the safe zone will be small, when it has a high value safe zone will be big
        # shrink_radius_by = random.uniform(*self.outer_circle_radius, self.radius - (self.radius / 100))
        shrink_radius_by = self.radius - (self.radius / 1000)
        self.pos_x = self.radius * math.cos(new_angle) - (shrink_radius_by * math.cos(new_angle))
        self.pos_y = self.radius * math.sin(new_angle) - (shrink_radius_by * math.sin(new_angle))

        global outer_circles
        for i in range(0, self.outer_circle_count):
            # outer_circles[i] represents body of the outer circle

            new_pos_x = self.pos_x + (self.radius - shrink_radius_by) * math.cos(outer_circles[i].angle)
            new_pos_y = self.pos_y + (self.radius - shrink_radius_by) * math.sin(outer_circles[i].angle)

            outer_circles[i].position = new_pos_x, new_pos_y

        self.radius = shrink_radius_by


def initialize_safe_zone(pos_x=0, pos_y=0):
    global safe_zone_instance

    safe_zone_instance = SafeZone(pos_x, pos_y)
