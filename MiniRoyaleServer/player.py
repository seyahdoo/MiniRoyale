from Inventory.inventory import Inventory
import Inventory.Items.item as item
import random
import threading
import director
import bullet
import pymunk
import pickup
from math import radians
from pymunk import Vec2d
from math import degrees
import client

import physics

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

        self.movement_speed = 0
        self.health = 100
        self.dead = False
        self.name = "Unknown"

        self.dropout_time = 0
        self.last_packet_id = 0
        self.sent_packet_id = 0

        # generate random player id and add it to the list
        # TODO make player id count from 0-inf incremented (like prop_id)
        player_id = random.randint(1, 5000)
        with players_lock:
            while player_id in players:
                player_id = random.randint(1, 5000)
            players[player_id] = self
            self.player_id = player_id

        self.inventory = Inventory()
        print("player initiated, id:{}".format(self.player_id))

        self.add_cheat_items_for_testing()
        print("player cheat items, id:{}".format(self.player_id))

        # physics stuff
        self.body = None
        self.shape = None
        self.body = pymunk.Body(10, pymunk.inf)

        self.shape = pymunk.Circle(self.body, 0.55)
        self.shape.elasticity = 0
        self.shape.collision_type = physics.collision_types["player"]

        player_shape_to_player[self.shape] = self

        with players_lock:

            self.create_body()
            players[self.player_id] = self

        global total_player_count
        global alive_player_count

        with total_player_count_lock:
            total_player_count += 1

        with alive_player_count_lock:
            alive_player_count += 1

        print("player body initiated, id:{}".format(self.player_id))

    def move(self, packet_id, pos_x, pos_y, angle):
        # TODO computate max possible distance player can move since last move request
        # TODO and make this computation done by pymunk
        if self.dead:
            return
        # print("player_id:{} trying to move to ({},{})".format(str(self.player_id), str(pos_x), str(pos_y)))
        # drop packet id
        if self.last_packet_id > int(packet_id):
            return
        else:
            self.last_packet_id = int(packet_id)
        try:
            self.body.position = Vec2d(float(pos_x), float(pos_y))
            self.body.angle = radians(float(angle))
        except:
            print("Error: Can not parse position info. Playerid:{} ".format(self.player_id))

        # print("player_id:{} current position ({},{})".format(str(self.player_id), str(self.pos_x), str(self.pos_y)))

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

        bullet.Bullet(self.player_id, self.body.position[0], self.body.position[1], degrees(self.body.angle), speed,
                      damage)

    def on_bullet_hit(self, bullet_obj):
        self.health -= bullet_obj.damage
        print('got hit! ' + str(self.health))
        if self.health < 0:
            self.killed()

    def killed(self):
        self.health = 0
        self.dead = True
        print("im dead as {}".format(self.name))
        # send info to clients
        client.send_message_to_nearby_clients(self.body.position[0], self.body.position[1], "KILED:{}".format(self.player_id))

        with physics.physics_lock:
            physics.space.remove(self.body, self.shape)

        director.on_player_killed()

    def create_body(self):
        self.body = pymunk.Body(500, pymunk.inf)

        self.shape = pymunk.Circle(self.body, 0.55)
        self.shape.elasticity = 0
        self.shape.collision_type = physics.collision_types["player"]

        player_shape_to_player[self.shape] = self

        with physics.physics_lock:
            physics.space.add(self.body, self.shape)

    def pickup_item(self, pickup_id, quantity):
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
        player_information += str("PINFO:{},{},[{}];".format(player_id, p.name, p.inventory.get_item_list()))
        if p.dead:
            player_information += str("KILED:{};".format(player_id))
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


# Buraya bak
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
