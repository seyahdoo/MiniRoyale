import Inventory.Items.item as item
import bullet
import threading
import timeit
import time
import client
import player
import physics
import director

# Global Variables
game_instance = None


class Game:
    def __init__(self):
        print("initiating game")

        self.winner_player = None

        # TODO make tickrate global -> game.tick_rate
        self.tick_rate = 32

        physics.setup()

        # Spawn items
        director.spawn_items()
        director.spawn_props()
        print("initiated game")

        self.game_thread = threading.Thread(target=self.run)
        self.game_thread.daemon = True
        self.game_thread.start()

    def run(self):
        anti_tick_rate = 1/self.tick_rate
        while True:
            # get current time
            enter_time = timeit.default_timer()

            # Add clients to be added to client list
            if len(client.clients_to_be_added) > 0:
                client.add_clients_to_be_added()

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

            # Check whether game is over or not every time a specific event has occurred
            # Like when a player has died
            if self.winner_player is not None:
                print('Winner name and player_id: {}, {}'.format(self.winner_player.name, self.winner_player.player_id))
                self.winner_player = None
                director.game_restart()

            # TODO what if server don't have enough time to update
            # calculated_sleep < 0 !!!
            calculated_sleep = anti_tick_rate - (timeit.default_timer() - enter_time)
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

