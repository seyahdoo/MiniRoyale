from Inventory.Items.item import Item  # import your stuff

import random
import threading
import timeit
import time

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
        self.players_lock = threading.Lock()
        self.players = {}
        
        self.props = {}
        self.clients = {}
        self.clients_lock = threading.Lock()

        self.bullets = {}
        self.bullets_to_be_spawned = []
        self.spawned_item_list = {}

        print("initiated game")
        
        self.spawn_items()

        self.space = pymunk.Space()

        self.game_thread = threading.Thread(target=self.run)
        self.game_thread.daemon = True
        self.game_thread.start()

    def run(self):
        anti_tick_rate = 1/self.tick_rate
        while True:
            delete = []
            # get current time
            enter_time = timeit.default_timer()

            # Get current actions
            # Create new bullets
            for current_bullet in self.bullets_to_be_spawned:
                bullet_id = self.prop_id_counter
                self.prop_id_counter += 1
                current_bullet.bullet_id = bullet_id

                self.bullets[bullet_id] = current_bullet
                self.space.add(current_bullet.body, current_bullet.shape)
            self.bullets_to_be_spawned = []

            # move players

            # Update Physics
            self.space.step(anti_tick_rate)

            # Update Bullets
            for b_id, current_bullet in self.bullets.items():
                if not current_bullet.update():
                    # Mark for delete
                    delete.append(b_id)

            # Delete marked (timed out) bullets
            for i in delete:
                self.space.remove(self.bullets[i].body, self.bullets[i].shape)
                del self.bullets[i]
                print("Successfully deleted bullet")

            # TODO Implement thread safe client
            # Send updated game info to all players
            for addr, current_client in self.clients.items():
                current_client.send_game_info()

            # TODO what if server dont have enough time to update
            # calculated_sleep < 0 !!!
            calculated_sleep = anti_tick_rate - (timeit.default_timer() - enter_time)
            if calculated_sleep > 0:
                time.sleep(calculated_sleep)

    def spawn_items(self):
        test_item_id = random.randint(1,5000)
        test_item_type = 1
        while self.spawned_item_list.get(test_item_id) is not None:
            test_item_id = random.randint(1,5000)
        self.spawned_item_list[test_item_id] = Item(test_item_id, test_item_type)
        
        # print("Successfully spawned an item with item_id:{}, item_type_id:{}".format(spawned_item_list[test_item_id].item_id,spawned_item_list[test_item_id].item_type_id))


def game_start():
    global game_instance
    game_instance = Game()


game_instance = None
