import Inventory.Items.item as item
import Inventory.Items.Weapons.weapon as weapon


class Inventory:
    def __init__(self):
        # If we don't include throwable weapons,
        # only items that can be flagged as equipped are weapons and armors and such!
        self.equipped_items = {}
        self.un_equipped_items = {}

        self.main_hand_item = None
        self.ammo_nine_mm_count = 5


    # TODO - Check if player is near enough to take an item from loot or spawnItem
    def add_item(self, item_id, item_type):
        # This section is for cheating purposes!
        # Switch item_type
        # 1001: Basic pistol
        # 1111: m4
        # 1102: ak47
        # 1113: m16
        # 1114: scar
        # 1201: m24

        item_name = None
        item_description = None

        if item_type == 1001:
            item_name = "G18"
            item_description = "Trusted weapons of officers because of it's strong power"
        elif item_type == 1111:
            item_name = "M4"
            item_description = "Trusted weapons of officers because of it's strong power"
        elif item_type == 1112:
            item_name = "AK47"
            item_description = "Trusted weapons of officers because of it's strong power"
        elif item_type == 1113:
            item_name = "M16"
            item_description = "Trusted weapons of officers because of it's strong power"
        elif item_type == 1114:
            item_name = "SCAR"
            item_description = "Trusted weapons of officers because of it's strong power"
        elif item_type == 1201:
            item_name = "M24"
            item_description = "Trusted weapons of officers because of it's strong power"

        self.equipped_items[item_id] = item.Item(item_id, item_type, item_name, item_description)
        print("Successfully equipped an item with item_id:{}, item_type_id:{}".format(self.equipped_items[item_id].item_id, self.equipped_items[item_id].item_type_id))

    def equip_item_to_main_hand(self, item_id):
        if self.equipped_items[item_id] is not None:
            self.main_hand_item = self.equipped_items[item_id]

    def get_item_list(self):
        items_in_inventory = ""
        for item_id in self.equipped_items.keys():
            items_in_inventory += "{}.".format(self.equipped_items[item_id].get_item_information())
        
        for item_id in self.un_equipped_items.items():
            items_in_inventory += "{}.".format(self.un_equipped_items[item_id].get_item_information())
        
        items_in_inventory = items_in_inventory[:-1]
        print("In inventory, the message is:{}".format(items_in_inventory))
        
        return items_in_inventory

    def get_weapon_used(self):
        return str(self.main_hand_item.item_name)
