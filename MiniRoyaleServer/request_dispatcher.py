import client
import game


def request_dispatcher(client_thread, buffer):
    # print("UDP: received:"+buffer)
    commands = buffer.split(';')    
    for cmd in commands:
        if cmd[0:5] == "MOVER":
            args = cmd[6:]
            args = args.split(',')
            
            # print(str(args))
            
            # if last packet number is > args[0] return
            client_thread.player.move(args[0], args[1], args[2], args[3])
            
        elif cmd[0:5] == "PONGO":
            # Successfull Ping-Pong relationship
            
            with client.ping_lock:
                # print(str(client_thread.player.dropout_time))
                client_thread.player.dropout_time = 0
            
        elif cmd[0:5] == "SAYYD":
            # Format of message
            player_message = str("SAID:{},".format(client_thread.player.player_id))
            # The message itself
            player_message += cmd[6:]
            # Closure
            player_message += str(";")
            print(player_message)
            client_thread.send(player_message)
            
        elif cmd[0:5] == "PCKEQ":
            item_id = cmd[6:]
            # print("equip request has come")
            client_thread.player.inventory.add_item(int(item_id))
        elif cmd[0:5] == "PIREQ":
            player_id = int(cmd[6:])
            player_information = ""
            if game.game_instance.players.get(player_id) is not None:
                player_information += str("PINFO:{},KekistPersonInTheTown,[{}];".format(player_id, game.game_instance.players[player_id].inventory.get_item_list()))
            # PINFO:12342,SnowDaddy,[232323+1.3332131+2]
            print(player_information)
            client_thread.send(player_information)
            
        elif cmd[0:5] == "SHOOT":
            # player_id = client_thread.player.player_id
            
            client_thread.player.shoot()
            print("Succesfull shoot action!")

            # TODO, Create bullet class with neccessarry attributes
