import client
import game
#import timeit

min_lag = 10000
max_lag = 0
old_time = 0

def RequestDispatcher(client_thread, buffer):
    #print("UDP: received:"+buffer)
   # global min_lag
   # global max_lag
   # global old_time
    
    
   # current_time = timeit.default_timer()
    
    #lag = current_time - old_time
   # if lag < min_lag:
   #     min_lag = lag
   # if lag > max_lag:
    #    max_lag = lag
        
    #old_time = current_time
   # print("current lag:{}, min_lag ={}, max_lag ={}".format(lag, min_lag, max_lag))
        
        
    commands = buffer.split(';')    
    for cmd in commands:
        if(cmd[0:5] == "MOVER"):
            args = cmd[6:]
            args = args.split(',')
            
            #print(str(args))
            
            # if last packet number is > args[0] return
            client_thread.player.Move(args[0],args[1],args[2])
            
        elif(cmd[0:5] == "PONGO"):
            # Succesfull Ping-Pong relationship
            
            with client.ping_lock:
                #print(str(client_thread.player.dropout_time))
                client_thread.player.dropout_time = 0
            
        elif(cmd[0:5] == "SAYYD"):
            # Format of message
            player_message = str("SAID:{},".format(client_thread.player.player_id))
            # The message itself
            player_message += cmd[6:]
            # Closure
            player_message += str(";")
            print(player_message)
            client_thread.send(player_message)
            
        elif(cmd[0:5] == "PCKEQ"):
            item_id = cmd[6:]
            #print("equip request has come")
            client_thread.player.inventory.addItem(int(item_id))
        elif(cmd[0:5] == "PIREQ"):
            player_id = int(cmd[6:])
            player_information = ""
            if game.player_list.get(player_id) is not None:
                player_information += str("PINFO:{},KekistPersonInTheTown,[{}];".format(player_id,game.player_list[player_id].inventory.getItemList()))
           #  PINFO:12342,SnowDaddy,[232323+1.3332131+2]
            print(player_information)
            client_thread.send(player_information)

            
            
            
            
            