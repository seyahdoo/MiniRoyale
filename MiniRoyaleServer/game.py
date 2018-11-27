import bullet
import timeit
import time
import client
import player
import bot
import safe_zone
import threading
import physics
import random
import prop
import pickup


# Global Variables
game_instance = None

random_ammo_count = 256
random_square_prop_count = 128
random_circle_prop_count = 128

delta_time = 0.0


class Game:
    def __init__(self):
        print("initiating game")

        self.winner_player = None

        # TODO make tickrate global -> game.tick_rate
        self.tick_rate = 32

        physics.setup()

        safe_zone.initialize_safe_zone()

        # Spawn items
        spawn_items()
        spawn_props()

        spawn_bots()
        find_bots()

        print("initiated game")

        self.game_thread = threading.Thread(target=self.run)
        self.game_thread.daemon = True
        self.game_thread.start()

    def run(self):
        anti_tick_rate = 1/self.tick_rate
        while True:
            # get current time
            enter_time = timeit.default_timer()

            # Get current actions
            # Create new bullets
            # bullet.spawn_bullets_to_be_spawned()

            # move_request players

            # Update Physics
            physics.tick(anti_tick_rate)

            # Update Bullets, mark for delete if collision has occurred or timeout
            bullet.update_bullet_state()

            # Delete marked (timed out) bullets
            # bullet.delete_marked_bullets()

            # Send updated game info to all players
            client.send_game_info_to_all_clients()

            # Send updated game info to all bots
            # bot.send_game_info_to_all_bots()

            # Move bots
            bot.step_all_bots()

            # Check whether game is over or not every time a specific event has occurred
            # Like when a player has died
            # TODO optimize this, make it into a function
            if self.winner_player is not None:
                print('Winner name and player_id: {}, {}'.format(self.winner_player.name, self.winner_player.player_id))
                self.winner_player = None
                finalize_game()
                # game_restart()

            # Shrink safe zone
            safe_zone.safe_zone_instance.shrink_safe_zone()

            global delta_time
            # TODO what if server don't have enough time to update
            # calculated_sleep < 0 !!!
            delta_time = timeit.default_timer() - enter_time
            calculated_sleep = anti_tick_rate - delta_time
            # print('Time passed: {}'.format((timeit.default_timer() - enter_time)))
            if calculated_sleep > 0:
                time.sleep(calculated_sleep)

        # print("Successfully spawned an item with item_id:{}, item_type_id:{}".format(spawned_item_list[test_item_id].item_id,spawned_item_list[test_item_id].item_type_id))


# Return True if the game is over else, return False
def game_logic():
    alive_player_count = player.get_alive_player_count()
    total_player_count = len(player.players)

    # If remaining player number is lower than 2, this means game is over
    if alive_player_count < 2 < total_player_count:
        game_instance.winner_player = player.get_winner_player()
        return True

    return False


def game_restart():
    player.grant_life_to_all_defilers()
    player.spawn_players()


def game_init():
    global game_instance
    game_instance = Game()

# TODO spawn items, props and such with fixed ranges in quantity distributed across regions of the maps
# For example: top left section -> 8-10 items with 6-7 props, bottom left section -> 7-8 items with 10-13 props and such


# Check whether game is over or not every time a specific event has occurred
# Like when a player has died
def on_player_killed():
    alive_player_count = player.alive_player_count

    # If remaining player number is lower than 2, this means game is over
    if alive_player_count < 2:
        game_instance.winner_player = player.get_winner_player()
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


def finalize_game():
    # For every client, send Disconnect message to them
    with client.clients_lock:
        for current_client in client.clients.values():
            current_client.disconnect()
