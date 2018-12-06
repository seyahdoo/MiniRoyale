import pymunk
import player
import bullet
import threading
import client
import sys

collision_types = {
    "player": 1,
    "bullet": 2,
    "prop": 3,
    "pickup": 4,
}

space = None

physics_lock = threading.Lock()


def setup():
    global space
    space = pymunk.Space()
    space.damping = 0.9

    # handler_[X Y]
    # X is first letter of collision first object's name
    # Y is first letter of collision second object's name
    handler_player_bullet = space.add_collision_handler(
        collision_types["player"],
        collision_types["bullet"])
    handler_player_bullet.begin = on_player_bullet_collision_begin

    handler_player_pickup = space.add_collision_handler(
        collision_types["player"],
        collision_types["pickup"])
    handler_player_pickup.begin = on_pickup_player_collision_begin

    handler_bullet_pickup = space.add_collision_handler(
        collision_types["bullet"],
        collision_types["pickup"])
    handler_bullet_pickup.begin = on_bullet_pickup_collision_begin

    handler_bullet_prop = space.add_collision_handler(
        collision_types["bullet"],
        collision_types["prop"])
    handler_bullet_prop.begin = on_bullet_prop_collision_begin


def tick(anti_tick_rate):
    global space
    space.step(anti_tick_rate)


def on_player_bullet_collision_begin(arbiter, space, data):
    bullet_shape = arbiter.shapes[1]
    # if 2 object collide at the same time
    if not bullet_shape:
        return

    bullet_obj = bullet.bullet_shape_to_bullet[bullet_shape]

    player_shape = arbiter.shapes[0]
    player_obj = player.player_shape_to_player[player_shape]

    # i shan't hit myself
    if bullet_obj.player_id == player_obj.player_id:
        return False

    player_obj.on_bullet_hit(bullet_obj)

    # Store bullet to be deleted object's necessary information
    deleted_bullet_info = "DELBL:{};".format(bullet_obj.bullet_id)
    deleted_bullet_pos_x = bullet_obj.body.position[0]
    deleted_bullet_pos_y = bullet_obj.body.position[1]
    print("-> Entering bullet lock from pyhsics, trying to handle collision")
    sys.stdout.flush()
    with bullet.bullets_lock:
        print("- entered bullet lock from pyhsics, trying to handle collision")
        if bullet_obj.bullet_id in bullet.bullets:
            with physics_lock:
                space.remove(bullet_obj.body, bullet_obj.shape)

            del bullet.bullets[bullet_obj.bullet_id]
            client.send_message_to_nearby_clients(deleted_bullet_pos_x, deleted_bullet_pos_y, deleted_bullet_info)
    print("<- exiting bullet lock from pyhsics, trying to handle collision")
    # mark bullet to be deleted
    # bullet.bullet_indexes_to_be_deleted.append(bullet_obj.bullet_id)

    return False


def on_pickup_player_collision_begin(arbiter, space, data):
    return False


def on_bullet_pickup_collision_begin(arbiter, space, data):
    return False


def on_bullet_prop_collision_begin(arbiter, space, data):
    return True
    bullet_shape = arbiter.shapes[1]
    prop_shape = arbiter.shapes[0]

    # if 2 object collide at the same time
    if not bullet_shape:
        return
