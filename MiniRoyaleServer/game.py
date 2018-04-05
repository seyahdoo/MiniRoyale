import Inventory.Items.item as item
import bullet
import threading
import timeit
import time
import client
import pymunk

collision_types = {
    "player": 1,
    "bullet": 2,
    "prop": 3,
}


class Game:
    def __init__(self):
        print("initiating game")
        
        self.tick_rate = 32
        self.prop_id_counter = 0
        
        self.props = {}

        print("initiated game")

        self.space = pymunk.Space()
        # Spawn items
        item.spawn_items()

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
            bullet.spawn_bullets_to_be_spawned()

            # move players

            # Update Physics
            self.space.step(anti_tick_rate)

            # Update Bullets, mark for delete if collision has occurred or timeout
            bullet.update_bullet_state()

            # Delete marked (timed out) bullets
            bullet.delete_marked_bullets()

            # Send updated game info to all players
            client.send_game_info_to_all_clients()

            # TODO what if server don't have enough time to update
            # calculated_sleep < 0 !!!
            calculated_sleep = anti_tick_rate - (timeit.default_timer() - enter_time)
            if calculated_sleep > 0:
                time.sleep(calculated_sleep)

        # print("Successfully spawned an item with item_id:{}, item_type_id:{}".format(spawned_item_list[test_item_id].item_id,spawned_item_list[test_item_id].item_type_id))


def game_start():
    global game_instance
    game_instance = Game()


game_instance = None
