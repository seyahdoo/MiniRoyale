from Inventory.inventory import Inventory
import Inventory.Items.item as item
import random
import threading
import bullet
import pymunk
import pickup
import player
import game
from math import radians
from pymunk import Vec2d
from math import degrees
import client
import timeit
from math import sqrt

import physics

player_id_count = 10000
player_id_count_lock = threading.Lock()

players = {}
players_lock = threading.Lock()

player_shape_to_player = {}

alive_player_count = 0
alive_player_count_lock = threading.Lock()

total_player_count = 0
total_player_count_lock = threading.Lock()


class Player:

    def __init__(self, _client):
        global players
        global players_lock

        self.client = _client

        self.health = 100
        self.dead = False
        self.name = "Unknown"

        self.speed = 12.0

        self.dropout_time = 0
        self.last_packet_id = 0
        self.sent_packet_id = 0

        # generate random player id and add it to the list
        # TODO make player id count from 0-inf incremented (like prop_id)
        with player_id_count_lock:
            global player_id_count
            player_id_count += 1
            self.player_id = player_id_count

            with players_lock:
                players[self.player_id] = self

        self.inventory = Inventory()
        print("player initiated, id:{}".format(self.player_id))

        self.add_cheat_items_for_testing()
        print("player cheat items, id:{}".format(self.player_id))

        # physics stuff
        self.body = None
        self.shape = None
        self.body = pymunk.Body(10, pymunk.inf)

        self.shape = pymunk.Circle(self.body, 0.58)
        self.shape.elasticity = 0
        self.shape.collision_type = physics.collision_types["player"]

        player_shape_to_player[self.shape] = self

        with players_lock:

            self.create_body()
            players[self.player_id] = self

        # Give default names depending if player is bot or not
        if self.client is None:
            self.name = "Bot - {}".format(self.player_id - 10000)
        else:
            self.name = "Player - {}".format(self.player_id - 10000)

        global total_player_count
        global alive_player_count

        with total_player_count_lock:
            total_player_count += 1

        with alive_player_count_lock:
            alive_player_count += 1

        self.time_since_last_movement = 0
        print("player body initiated, id:{}".format(self.player_id))

    # Get Move request
    # Speed check if movement is possible
    # Move body
    def move_request(self, packet_id, pos_x, pos_y, angle):
        if self.dead:
            return
        # print("player_id:{} trying to move_request to ({},{})".format(str(self.player_id), str(pos_x), str(pos_y)))
        # drop packet id

        # Check whether player is a bot or not
        if self.client is not None:

            if self.last_packet_id > int(packet_id):
                return
            else:
                self.last_packet_id = int(packet_id)
            try:
                self.check_speed_and_move(pos_x, pos_y, angle)
            except:
                print("Error: Can not parse position info. Playerid:{} ".format(self.player_id))

    def check_speed_and_move(self, pos_x, pos_y, angle):
        movement_threshold = ((timeit.default_timer() - self.time_since_last_movement) * self.speed)
        distance_between_positions = sqrt(
            ((float(pos_x) - self.body.position[0]) ** 2) + ((float(pos_y) - self.body.position[1]) ** 2))

        if distance_between_positions <= movement_threshold:
            self.move_body(pos_x, pos_y, angle)
        else:
            if self.client is not None:
                to_reply = "MOVRJ:{},{};".format(self.body.position[0], self.body.position[1])
                self.client.send(to_reply)

        self.time_since_last_movement = timeit.default_timer()

    def move_body(self, pos_x, pos_y, angle):
        self.body.position = Vec2d(float(pos_x), float(pos_y))
        self.body.angle = radians(float(angle))

    def add_cheat_items_for_testing(self):
        with item.item_id_lock:
            item.item_id_counter += 1
            weapon_id = item.item_id_counter

        # Add pistol
        item_type = 1001

        self.inventory.add_item(weapon_id, item_type)
        self.inventory.equip_item_to_main_hand(weapon_id)
        # self.current_weapon_in_hand = self.inventory.equipped_items[weapon_id]
        # print("Weapon with weapon_id:{} and weapon_type:{} is currenty equipped in main hand".format(
        #     self.current_weapon_in_hand.item_id, self.current_weapon_in_hand.item_type_id))

    def shoot(self):
        if self.dead:
            return

        weapon_type_id = self.inventory.main_hand_item.item_type_id

        if self.inventory.ammo_nine_mm_count <= 0:
            return

        self.inventory.ammo_nine_mm_count -= 1

        speed = 1
        damage = 0

        if weapon_type_id == 1001:
            speed = 15
            damage = 55
        elif weapon_type_id == 1002:
            speed = 15
            damage = 20

        # Maybe player died after coming into this method, then body_position will be None, check for this
        if not self.dead:
            bullet.Bullet(self.player_id, self.body.position[0], self.body.position[1], degrees(self.body.angle), speed,
                          damage)

    def on_bullet_hit(self, bullet_obj):
        self.health -= bullet_obj.damage
        print('got hit! ' + str(self.health))
        if self.health < 0:
            self.killed(bullet_obj)

    def killed(self, cause_of_death):
        self.health = 0
        self.dead = True
        print("im dead as {}".format(self.name))
        # send info to clients

        # death_message = ""

        if isinstance(cause_of_death, bullet.Bullet):

            weapon_used = player.players.get(cause_of_death.player_id).inventory.get_weapon_used()
            killer_player_name = player.players.get(cause_of_death.player_id).name

            death_message = "KILED:{},{},{},{},{};".format(self.player_id, self.name, cause_of_death.player_id, killer_player_name, weapon_used)
        else:
            weapon_used = "Explosion"
            death_message = "KILED:{},{},{},{},{};".format(self.player_id, self.name, 0, "Mother Nature", weapon_used)

        client.send_death_info_to_all_players(death_message)

        with physics.physics_lock:
            physics.space.remove(self.body, self.shape)

        game.on_player_killed()

    def create_body(self):
        self.body = pymunk.Body(500, pymunk.inf)

        self.shape = pymunk.Circle(self.body, 0.55)
        self.shape.elasticity = 0
        self.shape.collision_type = physics.collision_types["player"]

        player_shape_to_player[self.shape] = self

        with physics.physics_lock:
            physics.space.add(self.body, self.shape)

        # self.body.position = Vec2d(random.uniform(-100, 100), random.uniform(-100, 100))
        self.body.position = Vec2d(random.uniform(-5, 5), random.uniform(-5, 5))

    def pickup_item(self, pickup_id, quantity):
        if not self.dead:
            print("Pickup item and quantity:{}, {}".format(pickup_id, quantity))

            if pickup.pickups[pickup_id].item_type == 5009:
                self.inventory.ammo_nine_mm_count += quantity

            elif pickup.pickups[pickup_id].item_type == 1001:
                with item.item_id_lock:
                    item.item_id_counter += 1
                    item_id = item.item_id_counter

                self.inventory.add_item(item_id, pickup.pickups[pickup_id].item_type)

            # TODO Make this in another function
            with pickup.pickup_lock:
                deleted_pickup_info = "PCKDL:{};".format(pickup.pickups[pickup_id].pickup_id)
                deleted_pickup_pos_x = pickup.pickups[pickup_id].body.position[0]
                deleted_pickup_pos_y = pickup.pickups[pickup_id].body.position[1]

                with physics.physics_lock:
                    physics.space.remove(pickup.pickups[pickup_id].body, pickup.pickups[pickup_id].shape)

                del pickup.pickups[pickup.pickups[pickup_id].pickup_id]

                # print(deleted_pickup_info + str(deleted_pickup_pos_x) + str(deleted_pickup_pos_y))
                client.send_message_to_nearby_clients(deleted_pickup_pos_x, deleted_pickup_pos_y, deleted_pickup_info)


def get_player_info_command_message(player_id):
    player_information = ""
    p = players.get(player_id)

    try:
        player_information += str("PINFO:{},{},[{}]".format(player_id, p.name, p.inventory.get_item_list()))
        if p.dead:
            player_information += str(",{};".format(True))
        else:
            player_information += str(",{};".format(False))
    except:
        pass

    return player_information


# Return the alive player number by checking status of "dead" variable
def get_alive_player_count():
    global players
    alive_player_count = 0

    for current_player in players.values():
        if not current_player.dead:
            alive_player_count += 1

    return alive_player_count


def get_winner_player():
    global players

    winner_player = None

    for current_player in players.values():
        if not current_player.dead:
            winner_player = current_player
            return winner_player

    return None


def grant_life_to_all_defilers():
    global players

    for current_player in players.values():
        current_player.dead = False
        current_player.health = 100
        current_player.create_body()

        # TODO Carry this to game_start() function
        current_player.body.position = Vec2d(random.uniform(-100, 100), random.uniform(-100, 100))

        global alive_player_count
        global total_player_count

        with alive_player_count_lock:
            with total_player_count_lock:
                alive_player_count = total_player_count


def spawn_players():
    global players
    copy_of_players = players.copy()

    for current_player in copy_of_players.values():
        current_player.body.position = Vec2d(random.uniform(-100, 100), random.uniform(-100, 100))
