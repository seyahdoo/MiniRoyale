import pymunk
import player
import bullet

collision_types = {
    "player": 1,
    "bullet": 2,
    "prop": 3,
}

space = None


def setup():
    global space
    space = pymunk.Space()

    h = space.add_collision_handler(
        collision_types["player"],
        collision_types["bullet"])
    h.begin = on_bullet_player_collision_begin


def tick(anti_tick_rate):
    global space

    thread_safe_remove_body()

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

    # mark bullet to be deleted
    bullet.bullet_indexes_to_be_deleted.append(bullet_obj.bullet_id)

    return False


# TODO remove body thread safely
def thread_safe_remove_body(body, shape):
    pass
