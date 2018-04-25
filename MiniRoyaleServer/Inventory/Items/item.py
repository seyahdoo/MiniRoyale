import threading


spawned_item_list = {}

item_id_counter = 0
item_id_lock = threading.Lock()


class Item:

    def __init__(self, item_id, item_type_id, item_name, item_description):
        self.item_name = item_name
        self.item_description = item_description
        self.item_id = item_id
        # print(type(item_type_id))
        self.item_type_id = int(item_type_id)

    def get_item_information(self):
        item_information = "{}+{}".format(self.item_id, self.item_type_id)
        # print(item_information)
        return item_information



