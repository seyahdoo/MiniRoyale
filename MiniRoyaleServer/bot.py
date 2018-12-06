import player
import bullet
import pickup
import prop
import random
import math
import timeit

bots = []


class Bot:

    def __init__(self):
        self.player = player.Player(None)
        bots.append(self)

        # self.step_counter = 1
        self.moving_direction = (0.0, 0.0)
        self.angle_direction = 0.0
        self.change_direction(self.player.speed / 2, 10)

        self.time_since_last_direction_change = timeit.default_timer()

    def step(self):
        if not self.player.dead:
            # get positions of near rivals (try to kill without being killed [try to kill if hp>50])
            # get position of safezone (try to stay in)
            # get position of near ammo (collect em [if ammo is short])
            # get position of near obstacles (dont get near them)

            # try to go into safezone
            # try to shoot at rivals
            # try to get closer to rivals if health > 50

            # do otherwise
            self.move()

            # collect ammo

            calculated_time = timeit.default_timer() - self.time_since_last_direction_change

            if calculated_time > 1:
                self.change_direction(self.player.speed / 2, 10)
                self.time_since_last_direction_change = timeit.default_timer()
            else:

                self.change_direction(self.player.speed / 20, 5)

            # Reset step counter every 1 second
            # if self.step_counter > game.game_instance.tick_rate:
            #     self.step_counter += 1
            # else:
            #     self.step_counter = 1

    # TODO When the safe zone is avaible and bot is not in the safe zone:
    # Use A* or Trace algorithm to make sure that bot prioritize to move in safe area
    # If bot is in the safe area, move randomly to find ammo, kill players and such
    # Look at this for ideas http://qiao.github.io/PathFinding.js/visual/
    def move(self):

        # # For 1 second, decide a direction and move in that direction
        # bot_speed = self.player.speed / 2
        # if self.step_counter == 1:
        #     step_size_x = random.uniform(-bot_speed, bot_speed)
        #     step_size_y = random.uniform(-bot_speed, bot_speed)
        # else:
        #     bot_speed /= 10
        #     step_size_x = random.uniform(-bot_speed, bot_speed)
        #     step_size_y = random.uniform(-bot_speed, bot_speed)

        # randomized_angle = math.degrees(self.player.body.angle) + random.uniform(-10, 10)

        bot_pos_x = self.player.body.position[0] + self.moving_direction[0]
        bot_pos_y = self.player.body.position[1] + self.moving_direction[1]
        bot_angle = math.degrees(self.player.body.angle) + self.angle_direction

        self.player.check_speed_and_move(bot_pos_x, bot_pos_y, bot_angle)

    def change_direction(self, speed_multiplier, angle_multiplier):
        self.moving_direction = (random.uniform(-speed_multiplier, speed_multiplier)), \
                                (random.uniform(-speed_multiplier, speed_multiplier))
        self.angle_direction = random.uniform(-angle_multiplier, angle_multiplier)

    def get_game_info(self, copy_of_bullets, copy_of_players, copy_of_pickup, copy_of_props):
        print("Bot with id:{} succesfully received game info".format(self.player.player_id))
        pass


def step_all_bots():
    global bots

    for current_bot in bots:
        current_bot.step()

    return


def send_game_info_to_all_bots():
    # TODO Check this
    print("-> Entering bullet lock from bot, trying to copy bullets")
    with bullet.bullets_lock:
        print("- entered bullet lock from bot, trying to copy bullets")
        copy_of_bullets = bullet.bullets.copy()
    print("<- Exiting bullet lock from bot, trying to copy bullets")
    with player.players_lock:
        copy_of_players = player.players.copy()
    with pickup.pickup_lock:
        copy_of_pickup = pickup.pickups.copy()
    with prop.props_lock:
        copy_of_props = prop.props.copy()

    global bots
    for current_bot in bots.values():
        current_bot.get_game_info(copy_of_bullets, copy_of_players, copy_of_pickup, copy_of_props)
    pass


def remove_bot(bot_obj):
    pass

