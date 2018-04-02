
class Item:

    def __init__(self, item_id, item_type_id):
        self.name = None
        self.item_id = item_id
        # print(type(item_type_id))
        self.item_type_id = int(item_type_id)
        
    def get_item_information(self):
        item_information = "{}+{}".format(self.item_id,self.item_type_id)
        # print(item_information)
        return item_information
