import Inventory.Items.item as item
import player
import game
import pickup
import random
import prop
import bot

random_ammo_count = 256
random_square_prop_count = 128
random_circle_prop_count = 128


# TODO spawn items, props and such with fixed ranges in quantity distributed across regions of the maps
# For example: top left section -> 8-10 items with 6-7 props, bottom left section -> 7-8 items with 10-13 props and such


# Check whether game is over or not every time a specific event has occurred
# Like when a player has died
def on_player_killed():
    alive_player_count = player.alive_player_count

    # If remaining player number is lower than 2, this means game is over
    if alive_player_count < 2:
        game.game_instance.winner_player = player.get_winner_player()
        # print('Winner name and player_id: {}, {}'.format(self.winner_player.name, self.winner_player.player_id))
        game_restart()
        return

    return


def spawn_items():
    # test_item_id = item.item_id_counter
    # item.item_id_counter += 1
    # test_item_type = 1
    # item.spawned_item_list[test_item_id] = item.Item(test_item_id, test_item_type, "boi", "bios")

    for i in range(0, random_ammo_count):
        pickup.Pickup(random.uniform(-100.0, 100.0), random.uniform(-100.0, 100.0), random.randint(15, 30), 5009)


def spawn_props():
    for i in range(0, random_square_prop_count):
        prop.Prop(0, 7001, random.uniform(-100.0, 100.0), random.uniform(-100.0, 100.0))
    for i in range(0, random_circle_prop_count):
        prop.Prop(0, 7002, random.uniform(-100.0, 100.0), random.uniform(-100.0, 100.0))


def spawn_bots():
    for i in range(10):
        bot.Bot()
    pass


def find_bots():
    with player.players_lock:
        copy_of_players = player.players.copy()

    for bott in copy_of_players.values():
        if bott.client is not None:
            bot.bots[bot.player_id] = bott


def game_restart():
    player.grant_life_to_all_defilers()