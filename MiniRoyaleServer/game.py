import sys
sys.path.append('./Inventory/Items')
import item    # import your stuff

#import os
#wd = os.getcwd()    # save current working directory
#os.chdir('./Inventory/Items')    # change to directory containing main.py
#os.chdir(wd)    # change back to directory containing sub.pyimport random

import random
import threading
import timeit
import time











# TODO BUNU DUZELT AMK
spawned_item_list = {}


















#bullets = {}

class Game():
    
    def __init__(self):
        print("initiating game")
        
        self.tickrate = 32
        
        self.players_lock = threading.Lock()
        self.players = {}
        
        self.props = {}
        self.clients = {}
        self.clients_lock = threading.Lock()

        self.bullets = {}
                
        print("initiated game")
        
        self.spawnItems()
        
        self.game_thread = threading.Thread(target=self.run)
        self.game_thread.daemon = True
        self.game_thread.start()
        
    def run(self):
        anti_tickrate = 1/self.tickrate
        while(True):
            delete = []
            # get current time
            enter_time = timeit.default_timer()
            
            for b_id, current_bullet in self.bullets.items():
                if current_bullet.update() == False:
                    # Mark for delete
                    delete.append(b_id)
                    
            # Delete marked bullets      
            for i in delete:
                del self.bullets[i]
                
            for addr, current_client in self.clients.items():
                current_client.sendGameInfo()
            
            calculated_sleep = anti_tickrate - (timeit.default_timer() - enter_time)
            if calculated_sleep > 0:
                time.sleep(calculated_sleep)
            
    def updateBullets(self):
         for b_id, current_bullet in self.bullets.items():
            current_bullet.update()
            
        
    def spawnItems(self):
        global spawned_item_list
        test_item_id = random.randint(1,5000)
        test_item_type = 1
        while spawned_item_list.get(test_item_id) is not None:
            test_item_id = random.randint(1,5000)
        spawned_item_list[test_item_id] = item.Item(test_item_id, test_item_type)
        
        #print("Succesfully spawned an item with item_id:{}, item_type_id:{}".format(spawned_item_list[test_item_id].item_id,spawned_item_list[test_item_id].item_type_id))


def GameStart():
    global game_instance
    game_instance = Game()
    

game_instance = None

