
spawned_item_list = {}
item_id_counter = 0


class Item:

    def __init__(self, item_id, item_type_id):
        self.name = None
        self.item_id = item_id
        # print(type(item_type_id))
        self.item_type_id = int(item_type_id)
        
    def get_item_information(self):
        item_information = "{}+{}".format(self.item_id, self.item_type_id)
        # print(item_information)
        return item_information


def spawn_items():
    global item_id_counter
    global spawned_item_list

    test_item_id = item_id_counter
    item_id_counter += 1
    test_item_type = 1
    spawned_item_list[test_item_id] = Item(test_item_id, test_item_type)
