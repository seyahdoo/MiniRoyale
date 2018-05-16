import client
import player


def request_dispatcher(client_thread, buffer):
    # print("UDP: received:"+buffer)
    commands = buffer.split(';')

    for cmd in commands:

        # Move request from player
        # MOVER:PacketID,posx,posy,rotation_angle;
        if cmd[0:5] == "MOVER":
            args = cmd[6:]
            args = args.split(',')
            
            # print(str(args))
            
            # if last packet number is > args[0] return
            client_thread.player.move_request(args[0], args[1], args[2], args[3])
            
        # Says im still alive, Pong
        # PONGO;
        elif cmd[0:5] == "PONGO":
            # Successful Ping-Pong relationship
            
            with client.ping_lock:
                # print(str(client_thread.player.dropout_time))
                client_thread.player.dropout_time = 0

        # Say message to connected Channel
        # SAYYD:playerid,message;
        elif cmd[0:5] == "SAYYD":
            # Format of message
            player_message = str("SAID:{},".format(client_thread.player.player_id))
            # The message itself
            player_message += cmd[6:]
            # Closure
            player_message += str(";")
            print(player_message)
            client_thread.send(player_message)

        elif cmd[0:5] == "PCKUP":
            args = cmd[6:]
            args = args.split(',')

            # print("equip request has come")
            client_thread.player.pickup_item(int(args[0]), int(args[1]))


        # Player info request
        # PIREQ:playerid;
        elif cmd[0:5] == "PIREQ":
            player_id = int(cmd[6:])
            player_information = player.get_player_info_command_message(player_id)
            # PINFO:12342,SnowDaddy,[232323+1.3332131+2]
            print("PINFO to incoming PIREQ: " + player_information)
            client_thread.send(player_information)

        # Shoot as connected player
        # SHOOT;
        elif cmd[0:5] == "SHOOT":

            client_thread.player.shoot()
            #print("Succesfull shoot action!")
