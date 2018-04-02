from Inventory.Items.item import Item  # import your stuff

import random
import threading
import timeit
import time


class Game:
    def __init__(self):
        print("initiating game")
        
        self.tick_rate = 32
        
        self.players_lock = threading.Lock()
        self.players = {}
        
        self.props = {}
        self.clients = {}
        self.clients_lock = threading.Lock()

        self.bullets = {}

        self.spawned_item_list = {}
        print("initiated game")
        
        self.spawn_items()
        
        self.game_thread = threading.Thread(target=self.run)
        self.game_thread.daemon = True
        self.game_thread.start()

    def run(self):
        anti_tick_rate = 1/self.tick_rate
        while True:
            delete = []
            # get current time
            enter_time = timeit.default_timer()
            
            for b_id, current_bullet in self.bullets.items():
                if not current_bullet.update():
                    # Mark for delete
                    delete.append(b_id)
                    
            # Delete marked bullets      
            for i in delete:
                del self.bullets[i]
                
            for addr, current_client in self.clients.items():
                current_client.send_game_info()
            
            calculated_sleep = anti_tick_rate - (timeit.default_timer() - enter_time)
            if calculated_sleep > 0:
                time.sleep(calculated_sleep)
            
    def update_bullets(self):
         for b_id, current_bullet in self.bullets.items():
            current_bullet.update()

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
