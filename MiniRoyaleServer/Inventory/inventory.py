import sys
sys.path.append('./Items')
import item    # import your stuffimport os

#import os
#wd = os.getcwd()    # save current working directory
#os.chdir('./Items')    # change to directory containing main.py  
#import item    # import your stuff
#os.chdir('..')    # change to directory containing main.py  
#os.chdir('..')    # change to directory containing main.py  
import game    # import your stuff
#os.chdir(wd)    # change back to directory containing sub.pyimport random


class Inventory:
    
    def __init__(self):
        # If we don't include throwable weapons, only items that can be flagged as equipped are weapons and armors and such!
        self.equipped_items = {}
        self.un_equipped_items = {}
        
        
        
        
    # TODO - Check if player is near enough to take an item from loot or spawnItem
    def addItem(self, item_id):
        #print("Player is trying to pick an item with item_id:{}".format(item_id))
        #print(game.spawned_item_list.get(item_id))
        
        
        if game.spawned_item_list.get(item_id) is not None:   
            #print("Trying to pick up item from spawn_item_list")
            self.equipped_items[item_id] = game.spawned_item_list[item_id]
            game.spawned_item_list.pop(item_id)
            print("Succesfully picked an item with item_id:{}, item_type_id:{}".format(self.equipped_items[item_id].item_id,self.equipped_items[item_id].item_type_id))
        
        # This section is for cheating purposes!
        self.equipped_items[item_id] = item.Item(item_id, 1001)
        print("Succesfully equipped an item with item_id:{}, item_type_id:{}".format(self.equipped_items[item_id].item_id,self.equipped_items[item_id].item_type_id))
        
    def getItemList(self):
        
        items_in_inventory = ""
        for item_id in self.equipped_items.keys():
            items_in_inventory += "{}.".format(self.equipped_items[item_id].get_item_information())
        
        for item_id in self.un_equipped_items.items():
            items_in_inventory += "{}.".format(self.un_equipped_items[item_id].get_item_information())
        
        items_in_inventory = items_in_inventory[:-1]
        print("In inventory, the message is:{}".format(items_in_inventory))
        
        return items_in_inventory