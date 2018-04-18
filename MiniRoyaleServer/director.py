
import player
import game


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


def game_restart():
    player.grant_life_to_all_defilers()