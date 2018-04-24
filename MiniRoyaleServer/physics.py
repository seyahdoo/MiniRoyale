import pymunk
import player
import bullet
import threading
import client

collision_types = {
    "player": 1,
    "bullet": 2,
    "prop": 3,
}

space = None

physics_lock = threading.Lock()


def setup():
    global space
    space = pymunk.Space()

    h = space.add_collision_handler(
        collision_types["player"],
        collision_types["bullet"])
    h.begin = on_bullet_player_collision_begin


def tick(anti_tick_rate):
    global space
    space.step(anti_tick_rate)


# Make bricks be removed when hit by ball
def on_bullet_player_collision_begin(arbiter, space, data):
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

    with physics_lock:
        space.remove(bullet_obj.body, bullet_obj.shape)

    with bullet.bullets_lock:
        del bullet.bullets[bullet_obj.bullet_id]
    # mark bullet to be deleted
    # bullet.bullet_indexes_to_be_deleted.append(bullet_obj.bullet_id)

    client.send_message_to_nearby_clients(deleted_bullet_pos_x, deleted_bullet_pos_y, deleted_bullet_info)

    return False
