import Inventory.Items.item as item
import player
import game
import pickup
import random
import prop


# Check whether game is over or not every time a specific event has occurred
# Like when a player has died
def on_player_killed():
    alive_player_count = player.alive_player_count

    # If remaining player number is lower than 2, this means game is over
    if alive_player_count < 2:
        game.game_instance.winner_player = player.get_winner_player()
        # print('Winner name and player_id: {}, {}'.format(self.winner_player.name, self.winner_player.player_id))
        game_restart()
        return

    return


def spawn_items():
    # test_item_id = item.item_id_counter
    # item.item_id_counter += 1
    # test_item_type = 1
    # item.spawned_item_list[test_item_id] = item.Item(test_item_id, test_item_type, "boi", "bios")
    for i in range(0, 5):
        pickup.Pickup(random.uniform(-3, 3), random.uniform(-3, 3), 5, 5009)


def spawn_props():
    # for i in range(0, 6):
    #     rand_x = random.uniform(-10, 10)
    #     rand_y = random.uniform(-10, 10)
    #     prop.Prop(0, 7001, rand_x, rand_y)
    #     print('prop coordinate x and y:' + str(rand_x) + ', ' + str(rand_y))
    for i in range(0, 6):
        prop.Prop(0, 7002, random.uniform(-10, 10), random.uniform(-10, 10))


def game_restart():
    player.grant_life_to_all_defilers()