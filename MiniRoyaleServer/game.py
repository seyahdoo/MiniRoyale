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
            delete = []
            # get current time
            enter_time = timeit.default_timer()

            # Get current actions
            # Create new bullets
            for current_bullet in bullet.bullets_to_be_spawned:
                bullet_id = self.prop_id_counter
                self.prop_id_counter += 1
                current_bullet.bullet_id = bullet_id

                bullet.bullets[bullet_id] = current_bullet
                self.space.add(current_bullet.body, current_bullet.shape)
            bullet.bullets_to_be_spawned = []

            # move players

            # Update Physics
            self.space.step(anti_tick_rate)

            # Update Bullets
            for b_id, current_bullet in bullet.bullets.items():
                if not current_bullet.update():
                    # Mark for delete
                    delete.append(b_id)

            # Delete marked (timed out) bullets
            for i in delete:
                self.space.remove(bullet.bullets[i].body, bullet.bullets[i].shape)
                del bullet.bullets[i]
                print("Successfully deleted bullet")

            # TODO Implement thread safe client
            # Send updated game info to all players
            for addr, current_client in client.clients.items():
                current_client.send_game_info()

            # TODO what if server dont have enough time to update
            # calculated_sleep < 0 !!!
            calculated_sleep = anti_tick_rate - (timeit.default_timer() - enter_time)
            if calculated_sleep > 0:
                time.sleep(calculated_sleep)

        
        # print("Successfully spawned an item with item_id:{}, item_type_id:{}".format(spawned_item_list[test_item_id].item_id,spawned_item_list[test_item_id].item_type_id))


def game_start():
    global game_instance
    game_instance = Game()


game_instance = None
