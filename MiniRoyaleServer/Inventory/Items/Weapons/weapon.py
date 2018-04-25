from .. import item


class Weapon(item.Item):

    def __init__(self, item_id, item_type_id, item_name, item_description, magazine_size):
        super.__init__(item_id, item_type_id, item_name, item_description)

        self.magazine_size = magazine_size
        self.current_magazine = 0

