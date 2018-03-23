import os
wd = os.getcwd()    # save current working directory
os.chdir('./Inventory/Items')    # change to directory containing main.py  
import item    # import your stuff
os.chdir(wd)    # change back to directory containing sub.pyimport random

import random
import threading

spawned_item_list = {}
player_list = {}

class Game():
    
    def __init__(self):
        print("initiating game")
        
        self.tickrate = 0.5
        
        self.players_lock = threading.Lock()
        self.players = {}
        
        self.props = {}
        
        self.bullets = {}
                
        print("initiated game")
        
        self.spawnItems()
        
        
        
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

